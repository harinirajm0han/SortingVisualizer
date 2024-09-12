import pygame
import random
import math

# Initialize pygame
pygame.init()

# Class to handle drawing and storing visual information
class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

# Function to draw the UI and title
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render("I - Insertion | B - Bubble | M - Merge | Q - Quick | K - Bucket", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)
    pygame.display.update()

# Function to draw the list bars
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i] 

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

# Function to generate a random list of values
def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

# Bubble Sort algorithm
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

# Insertion Sort algorithm
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while i > 0 and ((lst[i - 1] > current and ascending) or (lst[i - 1] < current and not ascending)):
            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i + 1: draw_info.RED}, True)
            yield True

    return lst

# Merge Sort algorithm
def merge_sort(draw_info, lst, left, right, ascending=True):
    if right <= left:
        return

    mid = (left + right) // 2
    yield from merge_sort(draw_info, lst, left, mid, ascending)
    yield from merge_sort(draw_info, lst, mid + 1, right, ascending)

    yield from merge(draw_info, lst, left, mid, right, ascending)

def merge(draw_info, lst, left, mid, right, ascending=True):
    left_copy = lst[left:mid + 1]
    right_copy = lst[mid + 1:right + 1]

    l = r = 0
    for i in range(left, right + 1):
        if l < len(left_copy) and (r >= len(right_copy) or (left_copy[l] < right_copy[r] and ascending) or (left_copy[l] > right_copy[r] and not ascending)):
            lst[i] = left_copy[l]
            l += 1
        else:
            lst[i] = right_copy[r]
            r += 1

        draw_list(draw_info, {i: draw_info.GREEN}, True)
        yield True

# Quick Sort algorithm
def quick_sort(draw_info, lst, left, right, ascending=True):
    if left >= right:
        return

    pivot_idx = partition(draw_info, lst, left, right, ascending)
    yield from quick_sort(draw_info, lst, left, pivot_idx - 1, ascending)
    yield from quick_sort(draw_info, lst, pivot_idx + 1, right, ascending)

def partition(draw_info, lst, left, right, ascending=True):
    pivot = lst[right]
    i = left - 1

    for j in range(left, right):
        if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
            yield True

    lst[i + 1], lst[right] = lst[right], lst[i + 1]
    draw_list(draw_info, {i + 1: draw_info.GREEN, right: draw_info.RED}, True)
    yield True

    return i + 1

# Bucket Sort algorithm
def bucket_sort(draw_info, ascending=True):
    lst = draw_info.lst
    max_val = max(lst)
    size = max_val // len(lst)

    buckets = [[] for _ in range(len(lst))]

    for i in range(len(lst)):
        j = lst[i] // size
        if j != len(lst):
            buckets[j].append(lst[i])
        else:
            buckets[len(lst) - 1].append(lst[i])

    for i in range(len(lst)):
        buckets[i] = sorted(buckets[i], reverse=not ascending)
        for val in buckets[i]:
            lst[i] = val
            draw_list(draw_info, {i: draw_info.GREEN}, True)
            yield True

# Main function to run the game loop and handle user input
def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                # Display sorting completion message
                draw_info.window.fill(draw_info.BACKGROUND_COLOR)
                complete_msg = draw_info.LARGE_FONT.render("Sorting Complete!", 1, draw_info.GREEN)
                draw_info.window.blit(complete_msg, (draw_info.width / 2 - complete_msg.get_width() / 2, draw_info.height / 2))
                pygame.display.update()
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = lambda draw_info, ascending: merge_sort(draw_info, draw_info.lst, 0, len(draw_info.lst) - 1, ascending)
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = lambda draw_info, ascending: quick_sort(draw_info, draw_info.lst, 0, len(draw_info.lst) - 1, ascending)
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_k and not sorting:
                sorting_algorithm = bucket_sort
                sorting_algo_name = "Bucket Sort"

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
