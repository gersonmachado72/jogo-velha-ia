import streamlit as st
import math
import numpy as np

# Funções Minimax e jogo (adaptado do notebook)
def print_board(board):
    # Usaremos st.write para representar
    pass

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def evaluate(board):
    if check_winner(board, 'X'):
        return 1
    if check_winner(board, 'O'):
        return -1
    return 0

def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score == 1 or score == -1:
        return score
    if is_full(board):
        return 0
    if is_maximizing:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, depth+1, False))
                    board[i][j] = ' '
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, depth+1, True))
                    board[i][j] = ' '
        return best

def best_move(board):
    best_val = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                move_val = minimax(board, 0, False)
                board[i][j] = ' '
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

# Interface Streamlit
st.set_page_config(page_title="Jogo da Velha IA", layout="centered")
st.title("🎮 Jogo da Velha contra IA (Minimax)")

if 'board' not in st.session_state:
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

def reset_game():
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.game_over = False
    st.session_state.winner = None

# Exibir tabuleiro como botões
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        label = st.session_state.board[i][j]
        if label == ' ':
            label = '⬜'
        with cols[j]:
            if st.button(label, key=f"{i}{j}"):
                if not st.session_state.game_over and st.session_state.board[i][j] == ' ':
                    # Jogada do humano (O)
                    st.session_state.board[i][j] = 'O'
                    if check_winner(st.session_state.board, 'O'):
                        st.session_state.game_over = True
                        st.session_state.winner = "Você venceu!"
                    elif is_full(st.session_state.board):
                        st.session_state.game_over = True
                        st.session_state.winner = "Empate!"
                    else:
                        # Jogada da IA (X)
                        ai_move = best_move(st.session_state.board)
                        if ai_move != (-1, -1):
                            st.session_state.board[ai_move[0]][ai_move[1]] = 'X'
                        if check_winner(st.session_state.board, 'X'):
                            st.session_state.game_over = True
                            st.session_state.winner = "IA venceu!"
                        elif is_full(st.session_state.board):
                            st.session_state.game_over = True
                            st.session_state.winner = "Empate!"

if st.session_state.game_over:
    st.markdown(f"## {st.session_state.winner}")
    st.button("🔄 Jogar novamente", on_click=reset_game)