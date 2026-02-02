import matplotlib.pyplot as plt
import random

def plot_arbitrary_lines(lines_data):
    """
    Plots an arbitrary number of lines on a Matplotlib chart,
    coloring each line differently.

    Args:
        lines_data (list of tuples): A list where each element is a tuple
                                      representing a line. Each line tuple
                                      should contain two (x, y) tuples:
                                      ((x_start, y_start), (x_end, y_end)).
                                      Example: [((0, 0), (1, 1)), ((0, 1), (1, 0))]
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    if not lines_data:
        print("No lines provided to plot.")
        ax.set_title("No Lines to Display")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        plt.grid(True)
        plt.show()
        return

    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')

    for i, ((x_start, y_start), (x_end, y_end)) in enumerate(lines_data):
        x_coords = [x_start, x_end]
        y_coords = [y_start, y_end]

        # Generate a random color for each line
        color = (random.random(), random.random(), random.random())

        ax.plot(x_coords, y_coords, color=color, linewidth=2, label=f'Line {i+1}')

        # Update min/max for auto-scaling
        min_x = min(min_x, x_start, x_end)
        max_x = max(max_x, x_start, x_end)
        min_y = min(min_y, y_start, y_end)
        max_y = max(max_y, y_start, y_end)

    # Add a small buffer to the limits
    x_buffer = (max_x - min_x) * 0.1 if (max_x - min_x) > 0 else 1
    y_buffer = (max_y - min_y) * 0.1 if (max_y - min_y) > 0 else 1
    ax.set_xlim(min_x - x_buffer, max_x + x_buffer)
    ax.set_ylim(min_y - y_buffer, max_y + y_buffer)


    ax.set_title("Arbitrary Lines Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box') # Ensure aspect ratio is equal
    plt.show()

if __name__ == "__main__":
    # Example usage:
    # Define your lines here. Each line is a tuple of (start_point, end_point)
    # where each point is (x, y).
    my_lines = [
        ((0, 0), (10, 10)),
        ((0, 10), (10, 0)),
        ((5, 0), (5, 10)),
        ((0, 5), (10, 5)),
        ((2, 2), (8, 8)),
        ((1, 9), (9, 1)),
        ((-3, -3), (-1, -1)), # Example with negative coordinates
        ((15, 5), (12, 8))     # Example with different range
    ]

    plot_arbitrary_lines(my_lines)

    # Example with no lines
    # plot_arbitrary_lines([])

    # Example with a single line
    # plot_arbitrary_lines([((1, 1), (5, 5))])
