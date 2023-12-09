import os
import uuid
# sales = {'Week 1': 1000, 'Week 2': 850, 'Week 3': 1250, 'Week 4': 200}
# sentiment_scores = {'Week 1': 0.5, 'Week 2': 0.3, 'Week 3': 0.55, 'Week 4': 0.6}
# Example dictionary of sales values per week

# Extract the weeks and sales values as separate lists
def generate_bar_graph(sales):
    import matplotlib.pyplot as plt3
    # Extract the weeks and sales values as separate lists
    weeks = list(sales.keys())
    sales_values = list(sales.values())
    colors = ['green' if l == 'positive' else 'red' if l == 'negative' else 'gray' for l in weeks]

    # Create a bar graph of the sales data
    fig, ax = plt3.subplots(figsize=(8, 6))
    ax.bar(weeks, sales_values, color=colors)
    for week, sales_value in sales.items():
        ax.text(week, sales_value, str(sales_value))
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Number of Reviews')
    ax.set_title('Sentiment vs Number of Reviews')
    filename = str(uuid.uuid4())

    # Save the bar graph as a PNG image file
    image_path = os.path.relpath(f'images/{filename}.png')
    fig.savefig(image_path)
    return image_path


# def generate_line_graph(sales, labels):
#     # Extract the weeks and sales values as separate lists
#     weeks = list(sales.keys())
#     sales_values = list(sales.values())

#     # Create a line graph of the sales data with markers
#     fig, ax = plt.subplots(figsize=(8, 6))
#     ax.plot(weeks, sales_values, marker='o')
#     for week, sales_value in sales.items():
#         ax.text(week, sales_value, str(sales_value))
#     filename = str(uuid.uuid4())
#     ax.set_xlabel(labels['x'])
#     ax.set_ylabel(labels['y'])
#     ax.set_title(labels['title'])

#     # Save the line graph as a PNG image file
#     image_path = os.path.relpath(f'images/{filename}.png')
#     plt.savefig(image_path)
#     return image_path

def generate_line_graph(sales, sentiment_scores):
    import matplotlib.pyplot as plt2

    # Extract the weeks and sales values as separate lists
    weeks = list(sales.keys())
    sales_values = list(sales.values())

    # Create a line graph of the sales data with markers
    fig, ax = plt2.subplots(figsize=(8, 6))
    ax.plot(weeks, sales_values, marker='o', label='Sales')
    for week, sales_value in sales.items():
        ax.text(week, sales_value, str(sales_value))

    # Add the sentiment scores to the graph
    sentiment_scores_values = list(sentiment_scores.values())
    ax2 = ax.twinx()
    ax2.plot(weeks, sentiment_scores_values, marker='s', color='green', label='Sentiment Score')
    for week, sentiment_score in sentiment_scores.items():
        ax2.text(week, sentiment_score, str(sentiment_score))

    # Set the labels and title of the graph
    ax.set_xlabel('Week')
    ax.set_ylabel('Sales & Score')
    ax.set_title('Weekly Sales and Sentiment Score')

    # Combine the legends of both lines
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper center')
    filename = str(uuid.uuid4())
    # Save the line graph as a PNG image file
    image_path = os.path.relpath(f'images/{filename}.png')
    fig.savefig(image_path)
    return image_path

def generate_aspect_graph(data):
    import matplotlib.pyplot as plt1
    images = []
    labels = ['Positive', 'Neutral', 'Negative']
    # sizes = [50, 10, 40]
    colors = ['#34ad65', '#f5c542', '#e74c3c']
    title_font = {'fontsize': 16, 'fontweight': 'bold'}

    # Create pie chart
    for aspect in data:
        fig, ax = plt1.subplots(figsize=(4,3))
        if (sum(data[aspect]) == 0):
            continue
        ax.pie(data[aspect],colors=colors,labels=labels,autopct=lambda x: '{:.0f}'.format(x*sum(data[aspect])/100), startangle=90)
        ax.set_title(aspect.title(), **title_font)
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        filename = str(uuid.uuid4())

        # Save the bar graph as a PNG image file
        image_path = os.path.relpath(f'images/{filename}.png')
        images.append(image_path)
        fig.savefig(image_path)

    return images