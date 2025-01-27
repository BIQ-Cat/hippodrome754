package main

import (
	"encoding/csv"
	"math"
	"os"
	"runtime"
	"testing"
	"unsafe"
)

func BenchmarkRayCasting(b *testing.B) {
	colorMapFile, err := os.Open("../color.csv")
	if err != nil {
		b.Fatalf("cannot open color map: %v", err)
		return
	}
	colorMap, err := csv.NewReader(colorMapFile).ReadAll()
	if err != nil {
		b.Fatalf("cannot read color map: %v", err)
		return
	}

	heightMapFile, err := os.Open("../height.csv")
	if err != nil {
		b.Fatalf("cannot open height map: %v", err)
		return
	}
	heightMap, err := csv.NewReader(heightMapFile).ReadAll()
	if err != nil {
		b.Fatalf("cannot read height map: %v", err)
		return
	}

	angle := math.Pi / 4
	fov := math.Pi / 6
	deltaAngle := fov / 800

	b.ResetTimer()

	var pinner runtime.Pinner
	for i := 0; i < b.N; i++ {
		pinner.Unpin()
		res := make([]*int, 800)
		data := make(chan result, 800)

		rayAngle := angle - (fov / 2)
		for i := 0; i < 800; i++ {
			go castRayNoCGo(i, Camera{0, 0, angle, 270, 40}, Screen{800, 450}, colorMap, heightMap, rayAngle, 2000, 980, data)
			rayAngle += deltaAngle
		}

		for i := 0; i < 800; i++ {
			line := <-data
			pinner.Pin(&line.value[0])
			res[line.index] = (*int)(unsafe.Pointer(&line.value[0]))
		}
	}
	pinner.Unpin()
}
