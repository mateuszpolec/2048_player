import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
from random import randint
import json

Game = True


driver = webdriver.Chrome('/mnt/d/Programs/Projekty/2048_player/chromedriver.exe')
driver.get('https://play2048.co/')

def get_max_value_from_tiles():
    list_of_tiles = list()
    element = driver.find_elements_by_xpath("//div[contains(@class, 'tile-position')]")
    for e in element:
        list_of_tiles.append(e.get_attribute("class"))
    return list_of_tiles

def modify_list_of_tiles(list_of_tiles_in):
    rows, cols = (4, 4) 
    list_of_tile_informations = [[0 for i in range(cols)] for j in range(rows)] 
    for element in list_of_tiles_in:
        for r in (("tile ", ""), ("tile-", ""), ("position-", ""), (" new", ""), ("-", ""), (" ", ",")):
            element = element.replace(*r)
        value = element[0:element.index(",")]
        pos = element[element.index(",")+1:]
        list_of_tile_informations[int(pos[0])-1][int(pos[1])-1] = int(value)
    return int(np.max(list_of_tile_informations))

def check_if_game_over():
    element = driver.find_elements_by_xpath("//div[contains(@class, 'game-over')]")
    if(element):
        driver.find_element_by_xpath('//a[contains(text(), "Try again")]').click()
        with open('results.json') as json_file: 
            data = json.load(json_file) 
            temp = data['three_moves_results']
            temp.append(moves)
            write_json(data)
        moves["highest-tile"] = 2
        moves["number_of_moves"] = 0

def write_json(data, filename='results.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

if __name__ == "__main__":
    print("Im working!")
    moves = {"number_of_moves": 0, "highest-tile": 2}
    main_window = driver.find_element_by_tag_name("body")
    while Game:
        main_window.send_keys(Keys.ARROW_UP)
        time.sleep(0.1)
        main_window.send_keys(Keys.ARROW_LEFT)
        time.sleep(0.1)
        main_window.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.1)
        moves["number_of_moves"] += 1
        moves["highest-tile"] = modify_list_of_tiles(get_max_value_from_tiles())
        check_if_game_over()
