import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    months_dict = dict()
    months_dict["Jan"] = 0
    months_dict["Feb"] = 1
    months_dict["Mar"] = 2
    months_dict["Apr"] = 3
    months_dict["May"] = 4
    months_dict["June"] = 5
    months_dict["Jul"] = 6
    months_dict["Aug"] = 7
    months_dict["Sep"] = 8
    months_dict["Oct"] = 9
    months_dict["Nov"] = 10
    months_dict["Dec"] = 11


    Boolean_conv = dict()
    Boolean_conv["TRUE"] = 1
    Boolean_conv["FALSE"] = 0

    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)

        ret_tuple = ([], [])
        for row in reader:

            evidence = []
            evidence.append(int(row[0]))
            evidence.append(float(row[1]))
            evidence.append(int(row[2]))
            evidence.append(float(row[3]))
            evidence.append(int(row[4]))
            evidence.append(float(row[5]))
            evidence.append(float(row[6]))
            evidence.append(float(row[7]))
            evidence.append(float(row[8]))
            evidence.append(float(row[9]))
            evidence.append(months_dict[row[10]])
            evidence.append(int(row[11]))
            evidence.append(int(row[12]))
            evidence.append(int(row[13]))
            evidence.append(int(row[14]))
            evidence.append(1 if row[15] == "Returning_Visitor" else 0)
            #print(row[16])
            evidence.append(Boolean_conv[row[16]])
            ret_tuple[0].append(evidence)
            ret_tuple[1].append(Boolean_conv[row[17]])

    return ret_tuple


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    total = 0
    total_sensitivity = 0
    total_specificity = 0
    sensitivity_count = 0
    specificity_count = 0

    sensitivity = 0
    specificity = 0

    for i in range(len(labels)):
        total += 1 

        if labels[i] == 1:
            total_sensitivity += 1
            if labels[i] == predictions[i]:
                sensitivity_count += 1
        else:
            total_specificity += 1
            if labels[i] == predictions[i]:
                specificity_count += 1
        
    sensitivity = (sensitivity_count / total_sensitivity ) 
    specificity = (specificity_count / total_specificity)

    return (sensitivity, specificity) 


if __name__ == "__main__":
    main()
