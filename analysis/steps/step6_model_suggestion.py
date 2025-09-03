from abc import ABC, abstractmethod
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Abstract Base class for Model Suggestion Strategy
#-------------------------------------------------------------------------------------------------#
class ModelSuggestionStrategy(ABC):
    @abstractmethod
    def suggest_model(self, df: pd.DataFrame, target: str = None):
        """
        Performs multivariate analysis to suggest appropriate models based on data characteristics
        
        Args:
            df (pd.DataFrame): The dataframe containing the data
            target (str): Optional name of the target variable
            
        Return: 
           None: This method visualizes relationships between features to help with model selection
        """
        pass

# Concrete strategy using PairPlots
#-------------------------------------------------------------------------------------------------#
class PairPlotsStrategy(ModelSuggestionStrategy):
    def suggest_model(self, df: pd.DataFrame, target: str = None):
        """
        Visualizes pairwise relationships in the dataset using pairplots to help suggest models
        
        Args:
            df (pd.DataFrame): The dataframe containing the data
            target (str): Optional name of the target variable for coloring points
            
        Return: 
           None: Displays pairplot showing relationships between all numerical features
        """
        plt.figure(figsize=(12, 8))
        if target and target in df.columns:
            sns.pairplot(df, hue=target, diag_kind='kde')
        else:
            sns.pairplot(df, diag_kind='kde')
        plt.suptitle("Pairwise Relationships - Model Suggestion", y=1.02)
        plt.show()
        
        print("Model Suggestions based on PairPlots:")
        print("- If clear separation in target classes visible: Consider classification models")
        print("- If linear relationships visible: Consider linear models")
        print("- If complex non-linear patterns: Consider tree-based or neural network models")

# Concrete strategy using Heatmap
#-------------------------------------------------------------------------------------------------#
class HeatmapStrategy(ModelSuggestionStrategy):
    def suggest_model(self, df: pd.DataFrame, target: str = None):
        """
        Visualizes feature correlations using a heatmap to help suggest models
        
        Args:
            df (pd.DataFrame): The dataframe containing the data
            target (str): Optional name of the target variable
            
        Return: 
           None: Displays correlation heatmap of numerical features
        """
        plt.figure(figsize=(12, 8))
        numerical_df = df.select_dtypes(include=['number'])
        corr = numerical_df.corr()
        
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, 
                   fmt='.2f', linewidths=0.5, cbar_kws={'shrink': 0.8})
        plt.title("Feature Correlation Heatmap - Model Suggestion")
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
        
        print("\nModel Suggestions based on Heatmap:")
        print("- High correlation with target: Good for linear models")
        print("- High multicollinearity: Consider regularization or feature selection")
        print("- Low feature correlations: May need complex models to capture patterns")

# Context class that uses ModelSuggestionStrategy
#-------------------------------------------------------------------------------------------------#
class ModelSuggester:
    def __init__(self, strategy: ModelSuggestionStrategy):
        """
        Initializes Model Suggester with specific suggestion strategy

        Args:
            strategy (ModelSuggestionStrategy): The strategy to be used 
        """
        self._strategy = strategy

    def set_strategy(self, strategy: ModelSuggestionStrategy):
        """
        Sets new strategy for the Model Suggester 

        Args:
            strategy (ModelSuggestionStrategy): The new strategy to use
        """
        self._strategy = strategy
    
    def execute_suggestion(self, df: pd.DataFrame, target: str = None):
        """
        Executes model suggestion using the current strategy

        Args:
            df (pd.DataFrame): The dataframe containing the data
            target (str): Optional name of the target variable
        """
        self._strategy.suggest_model(df, target)

# Example Usage
if __name__ == "__main__":
    # Create sample data
    df = pd.read_csv(r"C:\Users\Junior\Desktop\Predictive-Policing-Advisory\artifacts\data_ingestion\Kampala_Theft_Dataset.csv")
    
    # Initialize with PairPlots strategy
    model_suggester = ModelSuggester(PairPlotsStrategy())
    model_suggester.execute_suggestion(df, 'target')
    
    # Switch to Heatmap strategy
    model_suggester.set_strategy(HeatmapStrategy())
    model_suggester.execute_suggestion(df, 'target')