import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import functions as f

df = pd.read_csv("dataframe.csv", index_col=[0,1])
albuns = df.index.unique(level="álbum")
musics = df.index.unique(level="música")

print(f.maiores_menores_idx(df, "música", "álbum", "exibições", "./img/Grupo1/Resposta_i", 0))
print(f.maiores_menores_idx(df, "música", "álbum", "exibições", "./img/Grupo1/Resposta_i", 1))
print(f.maiores_menores_idx(df, "música", "álbum", "duração", "./img/Grupo1/Resposta_ii", 0))
print(f.maiores_menores_idx(df, "música", "álbum", "duração", "./img/Grupo1/Resposta_ii", 1))
mais_ouvidas = df[df["exibições"]!=0].sort_values(by="exibições", ascending=False)["exibições"].head()
menos_ouvidas = df[df["exibições"]!=0].sort_values(by="exibições")["exibições"].head()
grafico1 = sns.barplot(data=mais_ouvidas.reset_index(), x="exibições", y="música", hue="música")
grafico1.figure.savefig("./img/Grupo1/Resposta_iii/mais_ouvidas.png")
grafico1.get_figure().clf()
grafico2 = sns.barplot(data=menos_ouvidas.reset_index(), x="exibições", y="música", hue="música")
grafico2.figure.savefig("./img/Grupo1/Resposta_iii/menos_ouvidas.png")
grafico2.get_figure().clf()

mais_longas = df[df["duração"]!=0].sort_values(by="duração", ascending=False)["duração"].head()
mais_curtas = df[df["duração"]!=0].sort_values(by="duração")["duração"].head()
grafico1 = sns.barplot(data=mais_longas.reset_index(), x="duração", y="música", hue="música")
grafico1.figure.savefig("./img/Grupo1/Resposta_iv/mais_longas.png")
grafico1.get_figure().clf()
grafico2 = sns.barplot(data=mais_curtas.reset_index(), x="duração", y="música", hue="música")
grafico2.figure.savefig("./img/Grupo1/Resposta_iv/mais_curtas.png")
grafico2.get_figure().clf()

premiados = df.groupby("álbum").sum().sort_values(by=["prêmios", "indicações"], ascending=[False, False]).head()
grafico = premiados.reset_index().plot(x="álbum", y=["prêmios", "indicações"], kind="bar")
plt.xticks(rotation='horizontal')
plt.xticks(rotation=12)
grafico.figure.savefig("./img/Grupo1/Resposta_v/premiados.png")
grafico.get_figure().clf()

popularidade = sns.jointplot(data=df[df["duração"]>0].reset_index(), x="duração", y="exibições", kind="reg")
popularidade.figure.savefig("./img/Grupo1/Resposta_vi/popularidade.png")

# palavras mais comuns no título dos álbuns
print("Palavras mais comuns - título álbuns:\n", f.words(albuns).value_counts().head(), sep="")
print("Palavras mais comuns filtradas - título álbuns:\n", f.words_n_stopwords(albuns).value_counts().head(), sep="")
f.wordcloud(albuns, "img/Grupo3/wordcloud_albuns.png")

# palavras mais comuns no título das músicas
print("Palavras mais comuns - título músicas:\n", f.words(musics).value_counts().head(), sep="")
print("Palavras mais comuns filtradas - título músicas:\n", f.words_n_stopwords(musics).value_counts().head(), sep="")
f.wordcloud(musics, "img/Grupo3/wordcloud_musics.png")

print(f.words_freq(df, "álbum", "letra"))

# palavras mais comuns na letra das músicas de toda a discografia
lyrics = pd.Series(df["letra"].unique())
print("Palavras mais comuns - letra músicas:\n", f.words(lyrics).value_counts().head(), sep="")
print("Palavras mais comuns filtradas - letra músicas:\n", f.words_n_stopwords(lyrics).value_counts().head(), sep="")
f.wordcloud(lyrics, "img/Grupo3/wordcloud_lyrics.png")

# título de álbum é tema recorrente nas letras
print("Tema álbuns:\n", f.theme(albuns, lyrics).value_counts().head(), sep="")

# título de música é tema recorrente nas letras
print("Tema músicas:\n", f.theme(musics, lyrics).value_counts().head(), sep="")

# Qual é a quantidade média de palavras por música?
print("A média de palavras por música é:", f.words_avg(lyrics))

#Quais são os álbuns com maior e menor média de duração das músicas?
print(f.duracao_album(df))

#A quantidade de palavra está necessariamente relacionada ao tempo de duração da música? Retorne True se sim e False se não
print(f.palavras_duracao(df,lyrics,albuns))
