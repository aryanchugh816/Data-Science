import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

@st.cache(allow_output_mutation=True)
def load_data(df):

    df = pd.read_csv(df)
    return df

def predict_movies(movie_name, titles):

    titles.index = titles.iloc[:,0]

    movie_user_ratings = movie_matrix[movie_name]
    similar_to_movie = movie_matrix.corrwith(movie_user_ratings)

    corr_movie = pd.DataFrame(similar_to_movie, columns=["Correlation"])
    corr_movie = corr_movie.join(titles["Num of Rating"])
    corr_movie.dropna(inplace=True)

    if movie_name not in corr_movie[corr_movie["Num of Rating"] > 100].sort_values("Correlation",
                                                                                   ascending=False).index[:10]:
        predictions = corr_movie[corr_movie["Num of Rating"] > 100].sort_values("Correlation", ascending=False).iloc[
                      :10, :]

    else:
        predictions = corr_movie[corr_movie["Num of Rating"] > 100].sort_values("Correlation", ascending=False).iloc[
                      :11, :]
        predictions.drop([movie_name], inplace=True)

    predictions.drop(["Num of Rating"], axis=1, inplace=True)
    predictions.Correlation = round(predictions.Correlation * 100, 2)
    predictions.rename(columns={'Correlation': 'Similarity (in percentage)'}, inplace=True)

    return predictions

st.title("Movie Recommendation System")
st.subheader("This is a simple application of a content based recommendation system using just pandas and simple linear algebra concepts")
st.subheader(" ")
st.markdown("[Click here]() to see the code and feel free to browse my [Github repository](https://github.com/aryanchugh816/Data-Science) for more projects and articles related to machine learning")
st.subheader(" ")
st.subheader("This is the Movies Dataset, please feel free to browse it")

# Loading dataframes
movie_titles = load_data("Datasets/Movie_title_rating.csv")
movie_matrix = load_data("Datasets/Movie_matrix.csv")
st.dataframe(movie_titles)

movie_name = st.selectbox("Which movie have you just watched ? (Start typing...)", ([''] + list(movie_titles.iloc[:,0])))
if movie_name != '':
    st.subheader("Movie selected: " + movie_name)
    graph_option = st.radio("Visualize data of the selected movie", ("No Visualization", "Rating Distribution", "Rating Distribution differentiated by gender"))
    if graph_option == "Rating Distribution":
        sns.distplot(movie_matrix[movie_name], bins=10)
        plt.xlabel("Rating (Out of 5.0)")
        st.pyplot()

    elif graph_option == "Rating Distribution differentiated by gender":
        temp_df = pd.read_csv("Datasets/u.user", names=["user id", "age", "gender", "occupation", "zip code"], sep="\|")
        temp_df.drop(columns=["age", "occupation", "zip code", "user id"], inplace = True)
        temp_df["rating"] = movie_matrix[movie_name]
        sns.countplot(y="rating", data=temp_df, hue="gender", palette="Accent")
        st.pyplot()

    st.subheader("Recommended Movies:")
    predicted_movies = predict_movies(movie_name, movie_titles)
    st.dataframe(predicted_movies)




