import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
nltk.download("stopwords")
from nltk.corpus import stopwords

def maiores_menores_idx(df:pd.DataFrame, indice_idx: str, grupo_idx:str, coluna:str, path:str, opcao:int) -> pd.DataFrame:
   """Monta um DataFrame com os elementos de maiores e menores valores por grupo e salva suas visualizações no path 

   :param df: dataframe com indices individuais e multi-index
   :type df: pd.DataFrame
   :param indice_idx: nome do indice individual de cada elemento
   :type indice_idx: str
   :param grupo_idx: indice coletivo dos elementos
   :type grupo_idx: str
   :param coluna: nome da coluna a ser analisada
   :type coluna: str
   :param path: caminho da pasta aonde a img deve ser salva
   :type path: str
   :param opcao: 0 para retornar os menores elementos e 1 para os maiores
   :type opcao: int
   :return: retorna um df com os elementos de maiores e menores valores por grupo e salva suas visualizações no path
   :rtype: pd.DataFrame
   """ 
   mais_idx = []
   menos_idx = []
   grupos = df.index.unique(level=grupo_idx)
   for grupo in grupos:
      mais = df[df[coluna]>0].loc[grupo].sort_values(by=coluna, ascending=False).head()
      menos = df[df[coluna]>0].loc[grupo].sort_values(by=coluna).head()
      mais_idx += mais[coluna].index.tolist()
      menos_idx += menos[coluna].index.tolist()
      mais_e_menos = pd.concat([mais, menos], keys=["mais", "menos"])

      grafico = sns.barplot(data=mais_e_menos.reset_index(), x="level_0", y=coluna, hue=indice_idx)
      grafico.figure.savefig(f"{path}/{grupo}.png")
      grafico.get_figure().clf()

   if opcao == 0:
      return df[df.index.isin(menos_idx, level=indice_idx)]
   else:
      return df[df.index.isin(mais_idx, level=indice_idx)]

def words(series: pd.Series) -> pd.Series:
   """Cria série pandas com todas as palavras de series

   :param series: série cujas palavras serão retornadas como elementos de uma nova série
   :type series: pd.Series
   :return: série com todas as palavras presentes em "series" passado como parâmetro
   :rtype: pd.Series
   """ 
   words_series = []
   for element in series:
      for word in str(element).split():
         words_series.append(word)
   return pd.Series(words_series)
   
def words_n_stopwords(series: pd.Series) -> pd.Series:
   """Cria série pandas com as palavras de series que não são stopwords (i.e. pronomes e artigos)

   :param series: série cujas palavras serão filtradas e retornadas como elementos de uma nova série
   :type series: pd.Index
   :return: série com as palavras que não são stopwords
   :rtype: pd.Series
   """   
   stop_words = set(stopwords.words("english"))
   n_stopwords = [word for word in words(series) if word.casefold() not in stop_words]
   return pd.Series(n_stopwords)

def wordcloud(series: pd.Series, file: str):
   """Cria wordcloud de série

   :param series: série pandas cujas palavras geraram o wordcloud
   :type series: pd.Series
   :param file: diretrizes para salvar o wordcloud
   :type file: str
   """   
   string = " ".join(word for word in words(series)) # une todas as palavras em uma única str
   wordcloud = WordCloud().generate(string)
   wordcloud.to_file(file)

# palavras mais comuns na letra das músicas por álbum
def words_freq(df: pd.DataFrame, indice:str, coluna:str) -> pd.DataFrame:
   """função retorna um dataframe com as frequencias das palavras mais freqentes da coluna por índice

   :param df: dataframe com todas informações
   :type df: pd.DataFrame
   :param indice: nome do indice pelo qual as frequenciais devem ser agrupadas
   :type indice: str
   :param coluna: nome da coluna que contem as strings com as palavras a serem analisadas
   :type coluna: str
   :return: dataframe com as frequencias das palavras mais frequentes da coluna por indice
   :rtype: pd.DataFrame
   """  
   indices = df.index.unique(level=indice)
   words_df = []
   for album in indices:
      lyrics = df.loc[album][coluna].unique()

      words_lyrics = words(lyrics)
      words_freq = words_lyrics.value_counts().head().values
      words_idx = words_lyrics.value_counts().head().index.to_list()
      multi_idx = pd.MultiIndex.from_tuples([(album, x) for x in words_idx], names=[indice, "word"])
      words_df.append(pd.DataFrame(data=words_freq, index=multi_idx, columns=["freq"]))

   return pd.concat(words_df)

def nouns(series: pd.Series) -> pd.Series:
   """Cria série com todos substantivos presentes nos elementos da série passada como parâmetro

   :param series: série que terá seus elementos analisados
   :type series: pd.Series
   :return: série apenas com os substantivos presentes na série passada como parâmetro
   :rtype: pd.Series
   """   
   nouns = []
   for element in series:
      words = pos_tag(word_tokenize(str(element)))
      for word,pos in words:
         if pos.startswith('NN'):
               nouns.append(word)
   return nouns

def theme(series1: pd.Series, series2: pd.Series) -> pd.Series:
   """Checa se os substantivos de series1 estão na series2

   :param series1: série pandas que origina os temas (substantivos)
   :type series1: pd.Series
   :param series2: série pandas onde os temas(substantivos) serão procurados
   :type series2: pd.Series
   :return: série pandas com os temas (substantivos) da series1 presentes na series2, de acordo com a frequencia
   :rtype: pd.Series
   """   
   theme = []
   for noum in nouns(series1):
      for word in words(series2):
         if noum == word:
            theme.append(noum)
   theme = pd.Series(theme)
   return theme

#Perguntas criadas:
# Qual é a quantidade média de palavras por música?

def words_avg(series: pd.Series) -> float:
   """Calcula média de palavras entre os elementos de uma série

   :param series: série com as letras das músicas
   :type series: pd.Series
   :return: média de palavras por música
   :rtype: float
   """   
   return round(words(series).count()/series.count(), 2)

def duracao_album(df: pd.DataFrame) -> pd.Series:
   """Retorna uma série com o nome das músicas e suas durações em ordem decrescente

   :param df: dataframe que possui como um dos índices os nomes das músicas e uma de suas colunas é a duração da música
   :type df: pd.DataFrame
   :return: série com o nome das músicas e suas durações em ordem decrescente
   :rtype: pd.Series
   """  
   return (df[df["duração"]>0].groupby("álbum").mean().sort_values(by="duração")["duração"])

def palavras_duracao(df: pd.DataFrame, lyrics: pd.Series, albuns:pd.Series) -> bool:
   """Verifica se a quantidade de palavras esta relacionada com o tempo da música

   :param df: dataframe com todas informações
   :type df: pd.DataFrame
   :param lyrics: série com as letras das músicas
   :type lyrics: pd.Series
   :param albuns: serie com o nome dos álbuns
   :type albuns: pd.Series
   :return: retorna verdadeiro caso a quantidade de palavras esteja relacionada com a duração e falso caso não esteja 
   :rtype: bool
   """   
   duracao_list=[]
   for album in albuns:
      duracao = df.loc[album]['duração'].unique()
      duracao_list.append(duracao)

   duracao_musica = []
   for i in range(0,len(duracao_list)):
      for k in range(0,len(duracao_list[i])):
         if duracao_list[i][k] != 0:
            duracao_musica.append(duracao_list[i][k])
         else: 
            continue
   
   palavras_musica = []
   for i in range(0,len(lyrics)):
      qnt_palavras = len(str(lyrics[i]).split())
      if qnt_palavras >2:
         palavras_musica.append(qnt_palavras)
      else:
         continue
      
   musica_palavra_max = df[df['letra'] == lyrics[palavras_musica.index(max(palavras_musica))]]
   
   musica_duracao_max = df[df['duração'] == max(duracao_musica)]

   musica_palavra_min = df[df['letra'] == lyrics[palavras_musica.index(min(palavras_musica))]]
   
   musica_duracao_min = df[df['duração'] == min(duracao_musica)]

   if musica_duracao_max.equals(musica_palavra_max) or musica_duracao_min.equals(musica_palavra_min):
      return True
   else:
      return False
