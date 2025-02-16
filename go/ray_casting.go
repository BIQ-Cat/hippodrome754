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

*/
import "C"
import (
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
	value []int32
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
	colorMap []int32, heightMap []int32,
	mapWidth, mapHeight int,
	rayAngle float64, rayDistance float64, scaleHeight float64,
	res chan<- result,
) {
	drawing := make([]int32, screen.height)
	sin, cos := math.Sincos(float64(rayAngle))
	smallestY := int(screen.height)
	firstLine := true

	for z := 1.0; z < rayDistance; z++ {
		x := int(z*cos + float64(camera.x))
		if x < 0 || x >= mapWidth {
			continue
		}

		y := int(z*sin + float64(camera.y))
		if y < 0 || y >= mapHeight {
			continue
		}

		// magic formula to remove fish eye
		depth := z * math.Cos(float64(camera.angle)-rayAngle)

		heightOnMap := heightMap[x*mapHeight+y] & 0xFF
		heightOnScreen := int(float64(camera.height-C.double(heightOnMap))/depth*scaleHeight + float64(camera.pitch))

		if firstLine {
			smallestY = min(smallestY, heightOnScreen)
			firstLine = false
		}

		if heightOnScreen < 0 {
			heightOnScreen = 0
		}

		if heightOnScreen < smallestY {
			for screenY := heightOnScreen; screenY < smallestY; screenY++ {
				drawing[screenY] = colorMap[x*mapHeight+y]
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
	drawing := make([]int32, screen.height)
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
				drawing[screenY] = int32(must(strconv.ParseInt(colorMap[x][y], 16, 32)))
			}
			smallestY = heightOnScreen
		}
	}
	res <- result{index, drawing}
}

//export RayCasting
func RayCasting(camera C.Camera, screen C.Screen, deltaAngle C.double, scaleHeight C.int, rayDistance C.int, colorMap *int32, heightMap *int32, mapWidth C.int, mapHeight C.int, fov C.double) **int32 {
	pinner.Unpin()
	res := make([]*int32, screen.width)
	data := make(chan result, screen.width)

	rayAngle := camera.angle - (fov / 2)

	goColorMap := unsafe.Slice(colorMap, mapWidth*mapHeight)
	goHeightMap := unsafe.Slice(heightMap, mapWidth*mapHeight)

	for i := 0; i < int(screen.width); i++ {
		go castRay(i, camera, screen, goColorMap, goHeightMap, int(mapWidth), int(mapHeight), float64(rayAngle), float64(rayDistance), float64(scaleHeight), data)
		rayAngle += deltaAngle
	}

	for i := 0; i < int(screen.width); i++ {
		line := <-data
		pinner.Pin(&line.value[0])
		res[line.index] = (*int32)(unsafe.Pointer(&line.value[0]))
	}

	pinner.Pin(&res[0])
	return (**int32)(unsafe.Pointer(&res[0]))
}

func main() {}
