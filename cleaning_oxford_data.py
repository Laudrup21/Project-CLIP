# outils utiles à importer de ce fichier : (avec from accessing_data import *)
#   1) la liste des phrases : sentences
#   2) final_image_list : la liste des images qui sont dans le dossier et qui sont référencées dans le groundtruth (Oui toutes les images ne sont pas dans les deux, il n'y en a que 845 distinctes en commun)
#   3) la fonction test(sentence, img_name) qui renvoie True ou False selon si l'image donnée en argument
#      est bien dans la catégorie représentée par la phrase.
#      exemple : test("a good photo of ashmolean", "ashmolean_000303.jpg") renvoie True
#   IMPORTANT : un dossier groundtruth contenant les fichiers textes de correpondances un dossier oxbuild_images contenant les images doivent être au même endroit que ce script

import os

buildings = ["all souls", "ashmolean", "balliol", "bodleian", "christ_church", "cornmarket", "hertford", "keble", "magdalen", "pitt rivers", "radcliffe camera"]
adj_list = ["good", "OK", "junk"]
sentences = [f"a {a} photo of {b}" for a in adj_list for b in buildings]

# print(sentences)
sentence = sentences[1]
adj = sentence.split(" photo ")[0].split("a ")[1]
# print(adj)
# print(sentence)

def test(sentence, img_name):
    img_name = img_name.split(".jpg")[0]
    adj = sentence.split(" photo ")[0].split("a ")[1]
    # print("adj is ", adj)
    
    building = sentence.split(" of ")[1].replace(" ", "_")
    # print("building is ", building)
    
    path_list = [os.path.join("groundtruth", building + f"_{i}_" + a + ".txt") for i in range (1,6) for a in adj_list]  
    path_list+= [os.path.join("groundtruth", building + f"_{i}_" + "query.txt") for i in range(1, 6)]
    # print("path_list is ", path_list)

    for path in path_list:
        with open(path,'r') as f:
            for line in f:
                # print('\n',line,  img_name)
                # print(len(img_name))
                # print(len(line))
                if line[:-1].partition(" ")[0] == img_name: 
                    return True
    return False

# here we have: sentence = "a good photo of ashmolean"

print(test(sentence, "balliol_000085.jpg"))
# prints False

print(test(sentence, "ashmolean_000303.jpg"))
# prints True

print(test(sentence, "oxc1_ashmolean_000058.jpg"))
# prints True

res = [0]*10
img_list = os.listdir("oxbuild_images")
groundtruth_list = []
files = os.listdir("groundtruth")
for file in files:
    with open(os.path.join("groundtruth", file), 'r') as f:
        for line in f:
            groundtruth_list.append(str(line)[:-1].split(" ")[0]+".jpg")
            
# print(len(groundtruth_list))
# print(len(list(set(groundtruth_list))))

# print(len(img_list))
# print(len(list(set(img_list))))

# print(len(list(set(img_list) & set(groundtruth_list))))
final_image_list = list(set(img_list) & set(groundtruth_list))
print(len(final_image_list))

# à partir de là : tests inutiles ne lis pas forcément


def counting():
    path_list = [os.path.join("groundtruth", building.replace(" ", "_") + f"_{i}_" + a + ".txt") for i in range (1,6) for building in buildings for a in adj_list]  
    path_list+= [os.path.join("groundtruth", building.replace(" ", "_") + f"_{i}_" + "query.txt") for i in range(1, 6)for building in buildings]
    line_counter=0
    seen = set()
    for path in path_list:
        # print ("path is", path)
        with open (path, 'r') as f:
            for line in f:
                if not line in seen: 
                    seen.add(line)
                    line_counter += 1
    print(line_counter)

# counting()
# il y a plus d'images dans le groundtruth (5280) que dans le dataset (5063)
