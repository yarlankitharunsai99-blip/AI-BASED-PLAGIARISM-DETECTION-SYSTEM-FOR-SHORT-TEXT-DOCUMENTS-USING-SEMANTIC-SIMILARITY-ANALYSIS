"""
AI-Based Plagiarism Detection System
Detects plagiarism in short text documents using semantic similarity analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def generate_text_corpus(n_documents=100, random_state=42):
    """Generate synthetic text corpus for plagiarism detection"""
    np.random.seed(random_state)
    
    # Original documents
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
    similarity_scores = []
    
    for i in range(n_documents):
        doc_type = np.random.choice(['original', 'paraphrased', 'plagiarized'], p=[0.3, 0.4, 0.3])
        base_text = np.random.choice(original_texts)
        
        if doc_type == 'original':
            document = base_text
            label = 'Original'
            sim_score = 1.0
        elif doc_type == 'paraphrased':
            # Create paraphrased version
            words = base_text.split()
            np.random.shuffle(words)
            document = ' '.join(words[:len(words)//2]) + ' ' + base_text[len(base_text)//2:]
            label = 'Paraphrased'
            sim_score = np.random.uniform(0.6, 0.85)
        else:  # plagiarized
            # Create plagiarized version (high similarity)
            document = base_text + ' ' + np.random.choice(original_texts)
            label = 'Plagiarized'
            sim_score = np.random.uniform(0.85, 0.98)
        
        documents.append(document)
        labels.append(label)
        similarity_scores.append(sim_score)
    
    data = {
        'Document_ID': [f'DOC{i:04d}' for i in range(n_documents)],
        'Text': documents,
        'Document_Type': labels,
        'Max_Similarity_Score': similarity_scores,
        'Word_Count': [len(doc.split()) for doc in documents],
        'Unique_Words': [len(set(doc.lower().split())) for doc in documents]
    }
    
    return pd.DataFrame(data)

def calculate_semantic_similarity(texts):
    """Calculate semantic similarity between texts using TF-IDF"""
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix, vectorizer

def detect_plagiarism(corpus_df, similarity_threshold=0.7):
    """Detect plagiarism in corpus"""
    texts = corpus_df['Text'].tolist()
    similarity_matrix, vectorizer = calculate_semantic_similarity(texts)
    
    plagiarism_results = []
    
    for i in range(len(texts)):
        max_similarity = 0
        matched_doc_id = None
        
        for j in range(len(texts)):
            if i != j and similarity_matrix[i][j] > max_similarity:
                max_similarity = similarity_matrix[i][j]
                matched_doc_id = j
        
        plagiarism_flag = 'Yes' if max_similarity >= similarity_threshold else 'No'
        
        plagiarism_results.append({
            'Document_ID': corpus_df.iloc[i]['Document_ID'],
            'Similarity_Score': max_similarity,
            'Matched_Document': corpus_df.iloc[matched_doc_id]['Document_ID'] if matched_doc_id is not None else 'None',
            'Plagiarism_Detected': plagiarism_flag,
            'Confidence': max_similarity * 100
        })
    
    return pd.DataFrame(plagiarism_results), similarity_matrix

def plot_similarity_distribution(corpus_df):
    """Plot distribution of similarity scores"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(corpus_df['Max_Similarity_Score'], bins=25, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_xlabel('Similarity Score', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0].set_title('Distribution of Similarity Scores', fontsize=12, fontweight='bold')
    axes[0].axvline(0.7, color='red', linestyle='--', linewidth=2, label='Plagiarism Threshold (0.7)')
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].legend()
    
    # Box plot by document type
    doc_types = corpus_df['Document_Type'].unique()
    data_by_type = [corpus_df[corpus_df['Document_Type'] == dt]['Max_Similarity_Score'].values for dt in doc_types]
    bp = axes[1].boxplot(data_by_type, labels=doc_types, patch_artist=True)
    
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    
    axes[1].set_ylabel('Similarity Score', fontsize=11, fontweight='bold')
    axes[1].set_title('Similarity Distribution by Document Type', fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/plagiarism_similarity_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: plagiarism_similarity_distribution.png")
    plt.close()

def plot_detection_results(plagiarism_results):
    """Plot plagiarism detection results"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plagiarism detection count
    plagiarism_counts = plagiarism_results['Plagiarism_Detected'].value_counts()
    colors_pie = ['#2ecc71', '#e74c3c']
    axes[0, 0].pie(plagiarism_counts.values, labels=plagiarism_counts.index, autopct='%1.1f%%',
                   colors=colors_pie, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    axes[0, 0].set_title('Plagiarism Detection Results', fontsize=12, fontweight='bold')
    
    # Similarity score distribution
    axes[0, 1].hist(plagiarism_results['Similarity_Score'], bins=20, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0, 1].axvline(0.7, color='red', linestyle='--', linewidth=2, label='Threshold')
    axes[0, 1].set_xlabel('Similarity Score', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Similarity Score Distribution', fontsize=12, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Confidence distribution
    axes[1, 0].hist(plagiarism_results['Confidence'], bins=20, color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_xlabel('Confidence (%)', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Detection Confidence Distribution', fontsize=12, fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Scatter plot: Similarity vs Confidence
    colors_scatter = ['#e74c3c' if x == 'Yes' else '#2ecc71' for x in plagiarism_results['Plagiarism_Detected']]
    axes[1, 1].scatter(plagiarism_results['Similarity_Score'], plagiarism_results['Confidence'],
                      c=colors_scatter, alpha=0.6, s=50, edgecolor='black', linewidth=0.5)
    axes[1, 1].set_xlabel('Similarity Score', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Confidence (%)', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Similarity vs Confidence', fontsize=12, fontweight='bold')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/plagiarism_detection_results.png', dpi=300, bbox_inches='tight')
    print("Saved: plagiarism_detection_results.png")
    plt.close()

def plot_similarity_heatmap(similarity_matrix, sample_size=20):
    """Plot similarity matrix heatmap"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Use subset for clarity
    sample_matrix = similarity_matrix[:sample_size, :sample_size]
    
    im = ax.imshow(sample_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax.set_xlabel('Document Index', fontsize=11, fontweight='bold')
    ax.set_ylabel('Document Index', fontsize=11, fontweight='bold')
    ax.set_title(f'Semantic Similarity Matrix (First {sample_size} Documents)', fontsize=12, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Similarity Score', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/plagiarism_similarity_heatmap.png', dpi=300, bbox_inches='tight')
    print("Saved: plagiarism_similarity_heatmap.png")
    plt.close()

def plot_word_count_analysis(corpus_df):
    """Plot word count analysis"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Word count by document type
    doc_types = corpus_df['Document_Type'].unique()
    word_counts_by_type = [corpus_df[corpus_df['Document_Type'] == dt]['Word_Count'].values for dt in doc_types]
    
    bp = axes[0].boxplot(word_counts_by_type, labels=doc_types, patch_artist=True)
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    
    axes[0].set_ylabel('Word Count', fontsize=11, fontweight='bold')
    axes[0].set_title('Word Count by Document Type', fontsize=12, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Unique words vs word count
    scatter = axes[1].scatter(corpus_df['Word_Count'], corpus_df['Unique_Words'],
                             c=corpus_df['Max_Similarity_Score'], cmap='RdYlGn',
                             alpha=0.6, s=50, edgecolor='black', linewidth=0.5, vmin=0, vmax=1)
    axes[1].set_xlabel('Total Word Count', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Unique Word Count', fontsize=11, fontweight='bold')
    axes[1].set_title('Word Diversity Analysis', fontsize=12, fontweight='bold')
    axes[1].grid(alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=axes[1])
    cbar.set_label('Similarity Score', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/plagiarism_word_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: plagiarism_word_analysis.png")
    plt.close()

def plot_tfidf_features(corpus_df):
    """Plot TF-IDF feature analysis"""
    texts = corpus_df['Text'].tolist()
    vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Get feature names and their average importance
    feature_names = vectorizer.get_feature_names_out()
    avg_importance = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
    
    # Sort by importance
    sorted_indices = np.argsort(avg_importance)[-15:]
    sorted_features = feature_names[sorted_indices]
    sorted_importance = avg_importance[sorted_indices]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(range(len(sorted_features)), sorted_importance, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_yticks(range(len(sorted_features)))
    ax.set_yticklabels(sorted_features, fontsize=10)
    ax.set_xlabel('Average TF-IDF Score', fontsize=11, fontweight='bold')
    ax.set_title('Top 15 Most Important Features (TF-IDF)', fontsize=12, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/plagiarism_tfidf_features.png', dpi=300, bbox_inches='tight')
    print("Saved: plagiarism_tfidf_features.png")
    plt.close()

def main():
    print("="*80)
    print("AI-BASED PLAGIARISM DETECTION SYSTEM - SEMANTIC SIMILARITY ANALYSIS")
    print("="*80)
    
    # Generate corpus
    print("\n[1] Generating text corpus...")
    corpus_df = generate_text_corpus(n_documents=100)
    corpus_df.to_csv('/home/ubuntu/plagiarism_corpus.csv', index=False)
    print(f"Corpus generated: {len(corpus_df)} documents")
    print(f"Document types: {corpus_df['Document_Type'].value_counts().to_dict()}")
    
    # Detect plagiarism
    print("\n[2] Detecting plagiarism using semantic similarity...")
    plagiarism_results, similarity_matrix = detect_plagiarism(corpus_df, similarity_threshold=0.7)
    plagiarism_results.to_csv('/home/ubuntu/plagiarism_detection_results.csv', index=False)
    print(f"Plagiarism detected: {(plagiarism_results['Plagiarism_Detected'] == 'Yes').sum()} documents")
    print(f"Average similarity score: {plagiarism_results['Similarity_Score'].mean():.4f}")
    
    # Generate visualizations
    print("\n[3] Generating visualizations...")
    plot_similarity_distribution(corpus_df)
    plot_detection_results(plagiarism_results)
    plot_similarity_heatmap(similarity_matrix)
    plot_word_count_analysis(corpus_df)
    plot_tfidf_features(corpus_df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()
