html = open('index.html', encoding='utf-8').read()
import re
print('Swiper Wrapper matches:', len(re.findall(r'<div class="swiper-wrapper">', html)))
print('Swiper Slides matches:', len(re.findall(r'<div class="swiper-slide">', html)))
print('Services images matches:', len(re.findall(r'/images/services/', html)))
