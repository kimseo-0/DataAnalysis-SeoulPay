import matplotlib.pyplot as plt

from collections import Counter
from PIL import Image
from wordcloud import WordCloud
import koreanize_matplotlib

def draw_wordcloud(word_list, 
                   most_common_count = -1, 
                   title = "wordcloud", 
                   font_path = "C:\Windodws\Fonts\malgun.ttf", 
                   image_path = "images/circle.png",
                   color_map = 'rainbow',
                   background_color = 'white'
                   ):
    """word_list를 받으면 Counter로 빈도 수를 센 후 워드 클라우드를 그리고 counter를 반환하는 함수"""
    counter = Counter(word_list)

    if most_common_count != -1:
        counter = counter.most_common(most_common_count)

    image = Image.open(image_path) # images/circle.png
    mask_img = np.array(image)
    
    wc = WordCloud(
        font_path = font_path, # C:\Windodws\Fonts\malgun.ttf
        mask=mask_img,
        background_color=background_color, # white
        colormap=color_map, # rainbow
        width=800,
        height=400
    )

    wc.generate_from_frequencies(counter)

    plt.figure(figsize=(5,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=15)
    plt.show()

    return counter