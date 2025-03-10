import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urljoin
import re

# url = 'https://books.toscrape.com/'
# response = requests.get(url)

# soup = BeautifulSoup(response.text, 'html.parser')

# # Fonction pour parcourir récursivement l'arbre DOM
# def traverse_dom (element, level=0):
#     #Afficher l'élément actuel
#     if element.name :
#         print(f"{' ' * level}<{element.name}>")
    
#     # Si l'élément a des enfants, les parcourir également
#     if hasattr(element, 'children'):
#         for child in element.children:
#             traverse_dom(child, level + 1)

# aside = soup.find('div', class_="side_categories")
# categories_div = aside.find("ul").find("li").find('ul')
# categories = [child.text.strip() for child in categories_div.children if child.name]

# images = soup.find_all('img')

# # Récupérer les titres complets de tous les livres

# # articles = soup.find_all('article', class_="product_pod")
# # for article in articles :
# #     link = article.find_all('a')[1]
# #     print(link.get('title'))

# # Méthode plus rapide

# title_tags = soup.find_all('a', title=True)
# titles = [a['title'] for a in title_tags]

# # Trouver les catégories de livres qui n'ont pas assez de livre (<5)
# with requests.Session() as session :
#     url = 'https://books.toscrape.com/'
#     response = session.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     aside = soup.find('div', class_="side_categories")
#     categories_div = aside.find("ul").find("li").find('ul')
#     categories = categories_div.find_all('a')
#     links = [a['href'] for a in categories]

#     seuil = 5

#     for category_link in links :
#         full_url = urljoin(url,category_link)
#         response = session.get(full_url)
#         category = BeautifulSoup(response.text, 'html.parser')
#         result_div = category.find('form','form-horizontal').find('strong')
#         result_number = int(result_div.text)
#         if result_number < seuil :
#             category_name_div = category.find('div', 'page-header action').find('h1')
#             category_name = category_name_div.text
#             print("La catégorie ",category_name, " n'a pas assez de livre.")

# Récupérer les livres (nom + identifiant) notés 1 étoile + gestion des erreurs

def trouver_livres_one (url) :
    try :
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Il y a eu un problème lors de l'accès au site : {e}")
        raise requests.exceptions.RequestException from e

    soup = BeautifulSoup(response.text, 'html.parser')
    all_books = soup.find_all('article', class_='product_pod')
    grades = [grade.find('p')['class'] for grade in all_books]
    title_tags = soup.find_all('a', title=True)
    titles = [a['title'] for a in title_tags]
    id_links = [a['href'] for a in title_tags]
    if len(titles) != len(grades) :
        print ("Error : pas autant de books que de grades")
    else : 
        k = 0
        while k < len(grades) : 
            if grades[k][1] == 'One' :
                title = titles[k]
                id_link_bis = id_links[k].split("_")
                id_link = id_link_bis[1].split("/")
                print('Le livre',title,"(id =",id_link[0],") n'a qu'une seule étoile.")
            k+=1
    next_button = soup.find('li', class_='next')
    if next_button != None :
        end_link = next_button.find('a')['href']
        full_url = urljoin(url,end_link)
        trouver_livres_one(full_url)

with requests.Session() as session :
    url = 'https://books.toscrape.com/'
    trouver_livres_one (url)