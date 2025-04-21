
import os
import sys
from PIL import Image
import math


def load_image(filename):
    img = Image.open(filename).convert('RGB')
    width, height = img.size
    pixels = list(img.getdata())
    matrix = []
    for i in range(height):
        row = []
        for j in range(width):
            index = i * width + j
            row.append(pixels[index])
        matrix.append(row)
    return matrix, width, height

def save_image(matrix, filename):
    height = len(matrix)
    width = len(matrix[0])
    img = Image.new('L', (width, height))
    flat_pixels = []
    for i in range(height):
        for j in range(width):
            flat_pixels.append(matrix[i][j])
    img.putdata(flat_pixels)
    img.save(filename)

def write_to_file(matrix, filename):
    f = open(filename, 'w')
    for i in range(len(matrix)):
        row = matrix[i]
        line = ''
        for j in range(len(row)):
            line += str(row[j])
            if j < len(row) - 1:
                line += ','
        f.write(line + '\n')
    f.close()

def grayscale(matrix):
    gray = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            pixel = matrix[i][j]
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            gray_value = int(0.3 * r + 0.59 * g + 0.11 * b)
            row.append(gray_value)
        gray.append(row)
    return gray

def gaussian_blur(matrix):
    kernel = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    kernel_size = 3
    kernel_sum = 0
    for i in range(3):
        for j in range(3):
            kernel_sum += kernel[i][j]

    height = len(matrix)
    width = len(matrix[0])
    blurred = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(0)
        blurred.append(row)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            total = 0
            for x in range(3):
                for y in range(3):
                    val = matrix[i + x - 1][j + y - 1]
                    total += val * kernel[x][y]
            blurred[i][j] = int(total / kernel_sum)

    return blurred

def edge_detection(matrix):
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    height = len(matrix)
    width = len(matrix[0])
    edges = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(0)
        edges.append(row)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            gx = 0
            gy = 0
            for x in range(3):
                for y in range(3):
                    val = matrix[i + x - 1][j + y - 1]
                    gx += val * sobel_x[x][y]
                    gy += val * sobel_y[x][y]
            magnitude = math.sqrt(gx ** 2 + gy ** 2)
            if magnitude > 100:
                edges[i][j] = 255
            else:
                edges[i][j] = 0

    return edges

def halftone(matrix):
    patterns = [
        [[0, 1], [1, 0]],
        [[1, 0], [0, 1]],
        [[1, 1], [0, 1]],
        [[1, 1], [1, 0]],
        [[1, 1], [1, 1]]
    ]
    height = len(matrix)
    width = len(matrix[0])
    new_height = 2 * height
    new_width = 2 * width
    halftone_image = []
    for i in range(new_height):
        row = []
        for j in range(new_width):
            row.append(0)
        halftone_image.append(row)

    for i in range(height):
        for j in range(width):
            level = matrix[i][j] * 4 // 255
            pattern = patterns[level]
            for x in range(2):
                for y in range(2):
                    if pattern[x][y] == 1:
                        halftone_image[2 * i + x][2 * j + y] = 255
                    else:
                        halftone_image[2 * i + x][2 * j + y] = 0

    return halftone_image

def floyd_steinberg(matrix):
    height = len(matrix)
    width = len(matrix[0])
    new_matrix = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(matrix[i][j])
        new_matrix.append(row)

    for i in range(height):
        for j in range(width):
            old_pixel = new_matrix[i][j]
            new_pixel = round(old_pixel / 16) * 16
            new_matrix[i][j] = new_pixel
            error = old_pixel - new_pixel

            if j + 1 < width:
                new_matrix[i][j + 1] += error * 7 / 16
            if i + 1 < height:
                if j > 0:
                    new_matrix[i + 1][j - 1] += error * 3 / 16
                new_matrix[i + 1][j] += error * 5 / 16
                if j + 1 < width:
                    new_matrix[i + 1][j + 1] += error * 1 / 16

    for i in range(height):
        for j in range(width):
            if new_matrix[i][j] > 255:
                new_matrix[i][j] = 255
            elif new_matrix[i][j] < 0:
                new_matrix[i][j] = 0
            else:
                new_matrix[i][j] = int(new_matrix[i][j])

    return new_matrix

import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <image_filename>")
        return

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    basename = os.path.splitext(os.path.basename(input_file))[0]

    matrix, width, height = load_image(input_file)

    gray_matrix = grayscale(matrix)
    save_image(gray_matrix, f'Grayscale_{basename}.png')
    write_to_file(gray_matrix, f'Grayscale_{basename}.txt')

    blurred_matrix = gaussian_blur(gray_matrix)
    edges_matrix = edge_detection(blurred_matrix)
    save_image(edges_matrix, f'Canny_{basename}.png')
    write_to_file(edges_matrix, f'Canny_{basename}.txt')

    halftone_matrix = halftone(gray_matrix)
    save_image(halftone_matrix, f'Halftone_{basename}.png')
    write_to_file(halftone_matrix, f'Halftone_{basename}.txt')

    floyd_matrix = floyd_steinberg(gray_matrix)
    save_image(floyd_matrix, f'FloydSteinberg_{basename}.png')
    write_to_file(floyd_matrix, f'FloydSteinberg_{basename}.txt')

    print("Processing complete.")


if __name__ == "__main__":
    main()
