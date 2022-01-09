# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# This file will hold ways of evaluating a given board position.
# This will mainly make use of the 'Basic Evaluation Features' outlined on 'https://www.chessprogramming.org/Evaluation'
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import GameLog
import PieceSquareTables


class Evaluator():
    def __init__(self, evaluator_choice):
        self.evaluator = evaluator_choice
        self.list_of_evaluators = ["simple"]
        self.fen_translator = GameLog.GameLog()

    def evaluate_board(self, board):
        match self.evaluator:
            case "simple":
                return self.simple_evaluator(board)

    def material_eval(self, board):
        # Board should just be the list, not the class.
        # Calculates the material score according to classical piece score evaluation.
        fen = self.fen_translator.translate_to_FEN(board)
        material_score = 900*(fen.count("K") - fen.count("k")) + 90*(fen.count("Q") - fen.count("q")) + 50*(fen.count("R") - fen.count(
            "r")) + 30*(fen.count("N") + fen.count("B") - fen.count("b") - fen.count("n")) + 10*(fen.count("P") - fen.count("p"))
        return material_score

    def get_psqr_table_eval(self, board):
        fen = self.fen_translator.translate_to_FEN(board)
        return PieceSquareTables.get_tablesquare_value(board, fen)

    def simple_evaluator(self, board):
        # Takes into account: material, piece square tables
        table_multiplyer = 0.2
        material_score = self.material_eval(board)
        psqtbl_score = self.get_psqr_table_eval(board)
        return material_score + table_multiplyer*psqtbl_score
