import sqlite3

def conectar():
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    return con

def obtenerPeliculas():
    con = conectar()
    c=con.cursor()
    query = "SELECT * FROM movies ORDER BY ranking ASC"
    resultado =c.execute(query)
    movies = resultado.fetchall()
    return movies

def obtenerDatoId(pk_id):
    con = conectar()
    c=con.cursor()
    query = "SELECT * FROM movies WHERE id = ?"
    resultado = c.execute(query, [pk_id])
    movie = resultado.fetchall()
    return movie
    

def obtenerRank(rank):
    con = conectar()
    c=con.cursor()
    query = "SELECT * FROM movies WHERE ranking = ?"
    resultado = c.execute(query, [rank])
    movie = resultado.fetchall()
    return movie

def actualizarDato(nombre, rank_nuevo):
    con = conectar()
    c=con.cursor()
    query = "UPDATE movies SET ranking = ? WHERE title = ?"
    c.execute(query, [rank_nuevo,nombre])
    con.commit()
