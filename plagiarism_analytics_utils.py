"""
Plagiarism Analytics Utilities
Generates detailed analytical datasets and insights for plagiarism detection
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

def generate_document_corpus(n_documents=100, random_state=42):
    """Generate comprehensive document corpus"""
    np.random.seed(random_state)
    
    original_texts = [
        "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
        "Natural language processing allows computers to understand and process human language.",
        "Deep learning uses neural networks with multiple layers to process complex patterns.",
        "Data science combines statistics, programming, and domain expertise to extract insights.",
        "Cloud computing provides on-demand access to computing resources over the internet.",
        "Cybersecurity protects computer systems and networks from unauthorized access.",
        "Blockchain technology enables secure and transparent distributed ledger systems.",
        "Internet of Things connects physical devices to the internet for data collection.",
        "Artificial intelligence is transforming industries through automation and intelligent systems.",
        "Big data analytics processes large volumes of data to discover meaningful patterns.",
        "Software engineering follows systematic approaches to design and develop applications.",
        "Web development creates interactive applications accessible through web browsers.",
        "Mobile applications provide services optimized for smartphones and tablets.",
        "Database management systems organize and retrieve data efficiently.",
        "Network protocols enable communication between computers and devices.",
        "Quantum computing uses quantum mechanics principles for computation.",
        "Augmented reality overlays digital information on the physical world.",
        "Virtual reality creates immersive digital environments for users.",
        "Computer vision enables machines to interpret and understand visual information.",
        "Robotics combines mechanical engineering with artificial intelligence."
    ]
    
    documents = []
    labels = []
    
    for i in range(n_documents):
        doc_type = np.random.choice(['original', 'paraphrased', 'plagiarized'], p=[0.3, 0.4, 0.3])
        base_text = np.random.choice(original_texts)
        
        if doc_type == 'original':
            document = base_text
            label = 'Original'
        elif doc_type == 'paraphrased':
            words = base_text.split()
            np.random.shuffle(words)
            document = ' '.join(words[:len(words)//2]) + ' ' + base_text[len(base_text)//2:]
            label = 'Paraphrased'
        else:
            document = base_text + ' ' + np.random.choice(original_texts)
            label = 'Plagiarized'
        
        documents.append(document)
        labels.append(label)
    
    data = {
        'Document_ID': [f'DOC{i:04d}' for i in range(n_documents)],
        'Text': documents,
        'Document_Type': labels,
        'Word_Count': [len(doc.split()) for doc in documents],
        'Unique_Words': [len(set(doc.lower().split())) for doc in documents],
        'Character_Count': [len(doc) for doc in documents]
    }
    
    return pd.DataFrame(data)

def analyze_document_statistics(corpus_df):
    """Analyze document statistics"""
    print("[1] Analyzing document statistics...")
    
    stats = []
    for doc_type in corpus_df['Document_Type'].unique():
        subset = corpus_df[corpus_df['Document_Type'] == doc_type]
        
        stats.append({
            'Document_Type': doc_type,
            'Document_Count': len(subset),
            'Avg_Word_Count': subset['Word_Count'].mean(),
            'Min_Word_Count': subset['Word_Count'].min(),
            'Max_Word_Count': subset['Word_Count'].max(),
            'Avg_Unique_Words': subset['Unique_Words'].mean(),
            'Avg_Character_Count': subset['Character_Count'].mean()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/plagiarism_document_statistics.csv', index=False)
    print("✓ Saved: plagiarism_document_statistics.csv")
    return stats_df

def analyze_text_complexity(corpus_df):
    """Analyze text complexity metrics"""
    print("[2] Analyzing text complexity...")
    
    complexity = []
    for idx, row in corpus_df.iterrows():
        text = row['Text']
        words = text.split()
        unique_words = len(set(w.lower() for w in words))
        
        # Lexical diversity (type-token ratio)
        lexical_diversity = unique_words / len(words) if len(words) > 0 else 0
        
        # Average word length
        avg_word_length = sum(len(w) for w in words) / len(words) if len(words) > 0 else 0
        
        # Sentence count (approximate)
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        if sentence_count == 0:
            sentence_count = 1
        
        complexity.append({
            'Document_ID': row['Document_ID'],
            'Lexical_Diversity': lexical_diversity,
            'Avg_Word_Length': avg_word_length,
            'Sentence_Count': sentence_count,
            'Words_Per_Sentence': len(words) / sentence_count
        })
    
    complexity_df = pd.DataFrame(complexity)
    complexity_df.to_csv('/home/ubuntu/plagiarism_text_complexity.csv', index=False)
    print("✓ Saved: plagiarism_text_complexity.csv")
    return complexity_df

def analyze_similarity_patterns(corpus_df):
    """Analyze similarity patterns"""
    print("[3] Analyzing similarity patterns...")
    
    texts = corpus_df['Text'].tolist()
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    patterns = []
    for i in range(len(texts)):
        similarities = []
        for j in range(len(texts)):
            if i != j:
                similarities.append(similarity_matrix[i][j])
        
        if similarities:
            patterns.append({
                'Document_ID': corpus_df.iloc[i]['Document_ID'],
                'Max_Similarity': max(similarities),
                'Min_Similarity': min(similarities),
                'Avg_Similarity': np.mean(similarities),
                'Std_Similarity': np.std(similarities),
                'High_Similarity_Count': sum(1 for s in similarities if s > 0.7)
            })
    
    patterns_df = pd.DataFrame(patterns)
    patterns_df.to_csv('/home/ubuntu/plagiarism_similarity_patterns.csv', index=False)
    print("✓ Saved: plagiarism_similarity_patterns.csv")
    return patterns_df

def generate_plagiarism_report(corpus_df):
    """Generate plagiarism detection report"""
    print("[4] Generating plagiarism report...")
    
    report = []
    
    report.append("AI-BASED PLAGIARISM DETECTION SYSTEM - ANALYSIS REPORT")
    report.append("="*80)
    
    report.append(f"\nTotal Documents Analyzed: {len(corpus_df)}")
    report.append(f"Document Type Distribution:")
    for doc_type, count in corpus_df['Document_Type'].value_counts().items():
        percentage = (count / len(corpus_df)) * 100
        report.append(f"  {doc_type}: {count} ({percentage:.1f}%)")
    
    report.append("\n\nDocument Characteristics:")
    report.append("-" * 80)
    report.append(f"Average Word Count: {corpus_df['Word_Count'].mean():.2f}")
    report.append(f"Average Unique Words: {corpus_df['Unique_Words'].mean():.2f}")
    report.append(f"Average Character Count: {corpus_df['Character_Count'].mean():.2f}")
    report.append(f"Word Count Range: {corpus_df['Word_Count'].min():.0f} - {corpus_df['Word_Count'].max():.0f}")
    
    report.append("\n\nDocument Type Analysis:")
    report.append("-" * 80)
    for doc_type in corpus_df['Document_Type'].unique():
        subset = corpus_df[corpus_df['Document_Type'] == doc_type]
        report.append(f"\n{doc_type}:")
        report.append(f"  Count: {len(subset)}")
        report.append(f"  Avg Word Count: {subset['Word_Count'].mean():.2f}")
        report.append(f"  Avg Unique Words: {subset['Unique_Words'].mean():.2f}")
    
    with open('/home/ubuntu/plagiarism_analysis_report.txt', 'w') as f:
        f.write('\n'.join(report))
    
    print("✓ Saved: plagiarism_analysis_report.txt")
    return report

def generate_sample_comparisons(corpus_df):
    """Generate sample document comparisons"""
    print("[5] Generating sample comparisons...")
    
    comparisons = []
    
    # Select diverse documents
    sample_docs = [
        corpus_df[corpus_df['Document_Type'] == 'Original'].iloc[0] if len(corpus_df[corpus_df['Document_Type'] == 'Original']) > 0 else corpus_df.iloc[0],
        corpus_df[corpus_df['Document_Type'] == 'Paraphrased'].iloc[0] if len(corpus_df[corpus_df['Document_Type'] == 'Paraphrased']) > 0 else corpus_df.iloc[1],
        corpus_df[corpus_df['Document_Type'] == 'Plagiarized'].iloc[0] if len(corpus_df[corpus_df['Document_Type'] == 'Plagiarized']) > 0 else corpus_df.iloc[2],
    ]
    
    for i, doc in enumerate(sample_docs):
        comparisons.append({
            'Comparison_ID': i + 1,
            'Document_ID': doc['Document_ID'],
            'Document_Type': doc['Document_Type'],
            'Word_Count': doc['Word_Count'],
            'Unique_Words': doc['Unique_Words'],
            'Text_Preview': doc['Text'][:100] + '...' if len(doc['Text']) > 100 else doc['Text']
        })
    
    comp_df = pd.DataFrame(comparisons)
    comp_df.to_csv('/home/ubuntu/plagiarism_sample_comparisons.csv', index=False)
    print("✓ Saved: plagiarism_sample_comparisons.csv")
    return comp_df

def main():
    print("="*80)
    print("PLAGIARISM ANALYTICS UTILITIES - GENERATING DETAILED DATASETS")
    print("="*80)
    print()
    
    # Generate main corpus
    print("Generating document corpus...")
    corpus_df = generate_document_corpus(n_documents=100)
    corpus_df.to_csv('/home/ubuntu/plagiarism_full_corpus.csv', index=False)
    print(f"✓ Corpus created: {len(corpus_df)} documents\n")
    
    # Generate analytical datasets
    analyze_document_statistics(corpus_df)
    analyze_text_complexity(corpus_df)
    analyze_similarity_patterns(corpus_df)
    generate_plagiarism_report(corpus_df)
    generate_sample_comparisons(corpus_df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All datasets generated successfully")
    print("="*80)

if __name__ == "__main__":
    main()
