import numpy as np
import pandas as pd

def generate_house_data(num_samples=1000, seed=42):
    np.random.seed(seed)
    
    # 1. Area in square feet (between 500 and 5000)
    area_sqft = np.random.randint(500, 5001, size=num_samples)
    
    # 2. Bedrooms: larger houses have more bedrooms (correlated)
    # Clip between 1 and 5
    bedrooms = np.clip(
        np.round(area_sqft / 900 + np.random.normal(0.2, 0.7, size=num_samples)),
        1, 5
    ).astype(int)
    
    # 3. Bathrooms: depends on number of bedrooms
    # Clip between 1 and 4
    bathrooms = np.clip(
        np.round(bedrooms * 0.8 + np.random.normal(0.1, 0.5, size=num_samples)),
        1, 4
    ).astype(int)
    
    # 4. Parking availability (0 for No, 1 for Yes)
    parking = np.random.choice([0, 1], size=num_samples, p=[0.35, 0.65])
    
    # 5. House age (between 0 and 50 years)
    house_age = np.random.randint(0, 51, size=num_samples)
    
    # 6. Price calculation (Base + linear combinations + interaction terms + noise)
    # Base price: ₹3,000,000 (30 Lakhs)
    # Area: ₹4,000 per sqft
    # Bedrooms: ₹500,000 each
    # Bathrooms: ₹300,000 each
    # Parking: ₹200,000 premium
    # Age: -₹30,000 per year
    base_price = 3000000
    price = (
        base_price + 
        (area_sqft * 4000) + 
        (bedrooms * 500000) + 
        (bathrooms * 300000) + 
        (parking * 200000) - 
        (house_age * 30000)
    )
    
    # Add random noise (normal distribution)
    noise = np.random.normal(0, 200000, size=num_samples)
    price = price + noise
    
    # Ensure minimum price is ₹2,000,000 (20 Lakhs)
    price = np.maximum(price, 2000000).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'area_sqft': area_sqft,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'parking': parking,
        'house_age': house_age,
        'price': price
    })
    
    return df

if __name__ == '__main__':
    print("Generating synthetic house price dataset...")
    df = generate_house_data()
    df.to_csv('house_data.csv', index=False)
    print(f"Dataset generated successfully! Saved 1000 records to 'house_data.csv'.")
    print(df.head())
