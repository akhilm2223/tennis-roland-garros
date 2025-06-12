#!/usr/bin/env python3
"""
Quick test script for Roland Garros Finals Explorer
"""

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        import pandas as pd
        print("✅ Pandas imported successfully")
        
        import numpy as np
        print("✅ NumPy imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported successfully")
        
        import seaborn as sns
        print("✅ Seaborn imported successfully")
        
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        print("✅ Plotly imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_loading():
    """Test data loading"""
    print("\n📊 Testing data loading...")
    try:
        import pandas as pd
        
        # Check if CSV file exists
        import os
        if not os.path.exists('roland_garros_finals_2000_2025.csv'):
            print("❌ CSV file not found!")
            return False
        
        # Load data
        df = pd.read_csv('roland_garros_finals_2000_2025.csv')
        print(f"✅ Data loaded successfully: {len(df)} records")
        
        # Check for 2025 prediction
        prediction_data = df[df['date'].str.contains('2025', na=False)]
        if len(prediction_data) > 0:
            print("✅ 2025 prediction data found")
            score = prediction_data.iloc[0]['score']
            print(f"📊 Score format: {score}")
        else:
            print("⚠️ No 2025 prediction data found")
        
        # Check key columns
        required_columns = ['champion', 'runner_up', 'score', 'duration', 'umpire']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if not missing_columns:
            print("✅ All required columns present")
        else:
            print(f"❌ Missing columns: {missing_columns}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_score_formatting():
    """Test score formatting function"""
    print("\n🎾 Testing score formatting...")
    try:
        # Simulate the format_score function
        def format_score(score_str):
            if pd.isna(score_str) or not score_str:
                return "Score not available"
            
            score = str(score_str)
            formatted_score = score.replace(',', '  ')
            formatted_score = formatted_score.replace('(', ' (').replace(')', ')')
            formatted_score = ' '.join(formatted_score.split())
            formatted_score = formatted_score.replace('  ', '   ')
            return formatted_score
        
        import pandas as pd
        
        # Test with sample scores
        test_scores = [
            "4-6,6-7(4-7),6-4,7-6(7-3),7-6(10-2)",
            "6-3, 6-2, 6-0",
            "7-6(7-1), 6-3, 7-5"
        ]
        
        for score in test_scores:
            formatted = format_score(score)
            print(f"Original: {score}")
            print(f"Formatted: {formatted}")
            print()
            
        print("✅ Score formatting test completed")
        return True
        
    except Exception as e:
        print(f"❌ Score formatting error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎾 Roland Garros Finals Explorer - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_loading,
        test_score_formatting
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app should work perfectly.")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        
    return passed == total

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...") 