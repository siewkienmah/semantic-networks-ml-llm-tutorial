"""Part B: calculate evaluation measures from slide examples; no dataset needed."""

LABELS = ["assign_technician", "escalate_now", "log_only"]
# Rows are actual classes; columns are predictions, both in LABELS order.
CONFUSION_MATRIX = [[15, 2, 8], [3, 2, 1], [8, 0, 21]]


def split_counts(total=240, test_fraction=0.25):
    """Return (training_count, test_count) for the supplied exercise totals."""
    # TODO B1: calculate the test count and subtract it from the total.
    raise NotImplementedError("Complete TODO B1")


def class_recall(matrix, class_index):
    """Return recall between 0 and 1; return 0.0 for an empty actual row."""
    # TODO B2: divide the diagonal entry by the sum of that actual-class row.
    raise NotImplementedError("Complete TODO B2")


def accuracy(matrix):
    """Return correct predictions / all predictions, or 0.0 for an empty matrix."""
    # TODO B3: sum the diagonal and divide by the sum of all cells.
    raise NotImplementedError("Complete TODO B3")


def macro_f1(matrix):
    """Return the unweighted mean of class F1 scores, using zero for undefined F1."""
    # TODO B4: for each class, get TP from the diagonal, FP from its column
    # excluding TP, and FN from its row excluding TP. F1 = 2TP/(2TP+FP+FN).
    # Average the scores equally; return 0.0 when the matrix is empty.
    raise NotImplementedError("Complete TODO B4")


if __name__ == "__main__":
    print("Training/test:", split_counts())
    for index, label in enumerate(LABELS):
        print(label, "recall:", class_recall(CONFUSION_MATRIX, index))
    print("Accuracy:", accuracy(CONFUSION_MATRIX))
    print("Macro-F1:", macro_f1(CONFUSION_MATRIX))
