class Constants:
    datasetFileName = "dataset.json"
    pathToInfeasibleZetaZeroes = "./infeasibleZetaZeroes.json"
    pathToCriticalZeroes = "./criticalZeroes.json"
    pathToGeneralValues = "./generalValues.json"
    INFINITE = 999999
    NEGATIVE_INFINITE = -INFINITE - 1
    PATH_TO_22000_INFERENCE_TEST_RESULT = "./inference/2200_inference_test.json"
    PATH_TO_22000_GENERATED_INFERENCE_INPUT = "./inference/2200_generated_inference_input.json"
    PATH_TO_INFERRENCE_STATS = "./inference/2200_generated_inference_stats.json"


class ExtractionConstants:
    choices = "choices"
    text = "text"
    inferredValue = "INFERRED_VALUE"
    expectedValue = "EXPECTED_VALUE"
    minDiff = "MIN_DIFF"
    maxDiff = "MAX_DIFF"
    mean = "MEAN"
    median = "MEDIAN"
    accuracy = "accuracy"
    statsAbout = "Stats about"
    inferrenceDiffs = "INFERRENCE_DIFFS"
    realPartStats = "Real Part Stats"
    imagPartStats = "Imaginary Part Stats"
