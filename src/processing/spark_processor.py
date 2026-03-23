#!/usr/bin/env python3
"""
PySpark Integration for Big Data Processing
Handles large-scale paper processing and analysis
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, explode, lower, when, size
import os

class SparkPaperProcessor:
    """Process large volumes of research papers using PySpark"""
    
    def __init__(self, app_name="AIResearchAssistant"):
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .master("local[*]") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()
        
        print(f"✅ Spark Session Created: {app_name}")
        print(f"   Master: {self.spark.sparkContext.master()}")
        print(f"   App ID: {self.spark.sparkContext.appId}\n")
    
    def process_papers_batch(self, papers_data):
        """
        Convert papers to Spark DataFrame and process at scale
        
        Args:
            papers_data: List of paper dictionaries
        
        Returns:
            Spark DataFrame with processed papers
        """
        # Convert to Spark DataFrame
        papers_df = self.spark.createDataFrame(papers_data)
        
        # Add new columns for analysis
        papers_df = papers_df.withColumn(
            "abstract_length", 
            size(split(col("abstract"), " "))
        )
        
        papers_df = papers_df.withColumn(
            "is_recent",
            when(col("year") >= 2024, 1).otherwise(0)
        )
        
        papers_df = papers_df.withColumn(
            "high_impact",
            when(col("citations") >= 50, 1).otherwise(0)
        )
        
        return papers_df
    
    def analyze_keywords(self, papers_df, keyword_list):
        """Analyze keyword frequency across all papers"""
        from pyspark.sql.functions import col, explode, split, count, desc
        
        print(f"🔍 Analyzing {len(keyword_list)} keywords...\n")
        
        # Extract abstracts and keywords
        for keyword in keyword_list:
            keyword_df = papers_df.filter(
                lower(col("abstract")).contains(keyword.lower())
            )
            count = keyword_df.count()
            print(f"  '{keyword}': mentioned in {count} papers")
        
        return papers_df
    
    def identify_research_clusters(self, papers_df):
        """Identify clusters of related research"""
        
        # Group by year and count papers
        yearly_stats = papers_df.groupBy("year").count() \
            .orderBy(desc("count")) \
            .collect()
        
        print("\n📊 Research Activity by Year:")
        for row in yearly_stats:
            print(f"   {row.year}: {row['count']} papers")
        
        # High-impact papers
        high_impact = papers_df.filter(col("high_impact") == 1).count()
        print(f"\n🏆 High-Impact Papers: {high_impact}")
        
        return papers_df
    
    def export_processed_data(self, papers_df, output_path="data/processed"):
        """Export processed data to multiple formats"""
        
        os.makedirs(output_path, exist_ok=True)
        
        # Parquet (fast, compressed)
        papers_df.write.mode("overwrite") \
            .parquet(f"{output_path}/papers.parquet")
        print(f"✅ Exported to: {output_path}/papers.parquet")
        
        # CSV for inspection
        papers_df.coalesce(1).write.mode("overwrite") \
            .option("header", "true") \
            .csv(f"{output_path}/papers.csv")
        print(f"✅ Exported to: {output_path}/papers.csv")
    
    def stop(self):
        """Stop Spark session"""
        self.spark.stop()
        print("✅ Spark session stopped")


if __name__ == "__main__":
    # Sample usage
    sample_papers = [
        {
            'title': 'Lithium-Ion Battery Recycling',
            'abstract': 'This paper explores recycling technologies for lithium-ion batteries used in electric vehicles',
            'source': 'semantic_scholar',
            'year': 2024,
            'citations': 150
        },
        {
            'title': 'Sustainable Battery Manufacturing',
            'abstract': 'Environmental impact of battery manufacturing and sustainability practices',
            'source': 'arxiv',
            'year': 2025,
            'citations': 89
        },
        {
            'title': 'Economic Viability of Recycling',
            'abstract': 'Economic analysis of battery recycling programs',
            'source': 'arxiv',
            'year': 2023,
            'citations': 45
        }
    ]
    
    # Process papers
    processor = SparkPaperProcessor()
    
    print("📥 Processing papers...\n")
    papers_df = processor.process_papers_batch(sample_papers)
    papers_df.show()
    
    print("\n" + "="*80)
    print("Analyzing keywords...")
    print("="*80)
    keywords = ['battery', 'recycling', 'sustainable', 'environmental']
    processor.analyze_keywords(papers_df, keywords)
    
    print("\n" + "="*80)
    print("Identifying research clusters...")
    print("="*80)
    processor.identify_research_clusters(papers_df)
    
    print("\n" + "="*80)
    print("Exporting processed data...")
    print("="*80)
    processor.export_processed_data(papers_df)
    
    processor.stop()
