package main

/*
typedef struct {
	double x;
	double y;
	double angle;
	double height;
	double pitch;
} Camera;

typedef struct {
	int width;
	int height;
} Screen;

typedef struct {
	char* colorMap;
	char* heightMap;
} Maps;
*/
import "C"
import (
	"bytes"
	"encoding/csv"
	"encoding/hex"
	"math"
	"runtime"
	"strconv"
	"unsafe"
)

type Camera struct {
	x, y   float64
	angle  float64
	height float64
	pitch  float64
}

type Screen struct {
	width, height int
}

type result struct {
	index int
	value []C.int
}

var pinner runtime.Pinner

func must[T any](value T, err error) T {
	if err != nil {
		panic(err)
	}
	return value
}

func castRay(
	index int,
	camera C.Camera, screen C.Screen,
	colorMap [][]string, heightMap [][]string,
	rayAngle float64, rayDistance float64, scaleHeight float64,
	res chan<- result,
) {
	drawing := make([]C.int, screen.height)
	sin, cos := math.Sincos(float64(rayAngle))
	smallestY := int(screen.height)
	firstLine := true

	for z := 1.0; z < rayDistance; z++ {
		x := int(z*cos + float64(camera.x))
		if x < 0 || x >= len(heightMap) {
			continue
		}

		y := int(z*sin + float64(camera.y))
		if y < 0 || y >= len(heightMap[0]) {
			continue
		}

		// magic formula to remove fish eye
		depth := z * math.Cos(float64(camera.angle)-rayAngle)

		heightOnMap := must(hex.DecodeString(heightMap[x][y][:4]))
		heightOnScreen := int(float64(camera.height-C.double(heightOnMap[0]))/depth*scaleHeight + float64(camera.pitch))

		if firstLine {
			smallestY = min(smallestY, heightOnScreen)
			firstLine = false
		}

		if heightOnScreen < 0 {
			heightOnScreen = 0
		}

		if heightOnScreen < smallestY {
			for screenY := heightOnScreen; screenY < smallestY; screenY++ {
				drawing[screenY] = C.int(must(strconv.ParseInt(colorMap[x][y], 16, 32)))
			}
			smallestY = heightOnScreen
		}
	}
	res <- result{index, drawing}
}

func castRayNoCGo(
	index int,
	camera Camera, screen Screen,
	colorMap [][]string, heightMap [][]string,
	rayAngle float64, rayDistance float64, scaleHeight float64,
	res chan<- result,
) {
	drawing := make([]C.int, screen.height)
	sin, cos := math.Sincos(float64(rayAngle))
	smallestY := int(screen.height)

	for z := 1.0; z < rayDistance; z++ {
		x := int(z*cos + float64(camera.x))
		if x < 0 || x >= len(heightMap) {
			continue
		}

		y := int(z*sin + float64(camera.y))
		if y < 0 || y >= len(heightMap[0]) {
			continue
		}

		// magic formula to remove fish eye
		depth := z * math.Cos(float64(camera.angle)-rayAngle)

		heightOnMap := must(hex.DecodeString(heightMap[x][y][:4]))
		heightOnScreen := int(float64(camera.height-float64(heightOnMap[0]))/depth*scaleHeight + float64(camera.pitch))

		if heightOnScreen < 0 {
			heightOnScreen = 0
		}

		if heightOnScreen < smallestY {
			for screenY := heightOnScreen; screenY < smallestY; screenY++ {
				drawing[screenY] = C.int(must(strconv.ParseInt(colorMap[x][y], 16, 32)))
			}
			smallestY = heightOnScreen
		}
	}
	res <- result{index, drawing}
}

//export RayCasting
func RayCasting(camera C.Camera, screen C.Screen, deltaAngle C.double, scaleHeight C.int, rayDistance C.int, maps C.Maps, fov C.double) **C.int {
	pinner.Unpin()
	res := make([]*C.int, screen.width)
	data := make(chan result, screen.width)

	rayAngle := camera.angle - (fov / 2)

	colorMap := must(csv.NewReader(bytes.NewBufferString(C.GoString(maps.colorMap))).ReadAll())
	heightMap := must(csv.NewReader(bytes.NewBufferString(C.GoString(maps.heightMap))).ReadAll())

	for i := 0; i < int(screen.width); i++ {
		go castRay(i, camera, screen, colorMap, heightMap, float64(rayAngle), float64(rayDistance), float64(scaleHeight), data)
		rayAngle += deltaAngle
	}

	for i := 0; i < int(screen.width); i++ {
		line := <-data
		pinner.Pin(&line.value[0])
		res[line.index] = (*C.int)(unsafe.Pointer(&line.value[0]))
	}

	pinner.Pin(&res[0])
	return (**C.int)(unsafe.Pointer(&res[0]))
}

func main() {}
