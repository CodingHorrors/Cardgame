import pandas


p = r"C:\Users\Alex\Documents\Programming\ProjectCardgame\test.csv"

new_names = input("Add one or multiple new names, seperated by ,\n>")
new_names = new_names.replace(" ","").split(",")
print(new_names)
with open(p, mode='a+', newline='') as score_file:
    data = {"Name" : new_names, "Score" : 0}
    score_panda = pandas.DataFrame(data=data)
    score_panda.to_csv(score_file)
    print(score_panda)
    score_panda.at[0,"Score"] += 1
    print(score_panda)
    won = int(score_panda[score_panda["Name"]=="Alex"].index.values)
    score_panda.at[won, "Score"] += 1
    print(score_panda)
