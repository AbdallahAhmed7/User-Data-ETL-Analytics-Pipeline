
#2_Analysis.py

import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt


# --------------------------------   Cleaning / Transformation   --------------------------------

print("############# Cleaning & Transformation Started ##########")

df = pd.read_csv('users.csv')

# ===================== 1. Handle Missing Values =====================
# maidenName contains many missing values → replace with 'Unknown'
df['maidenName'] = df['maidenName'].replace('', 'Unknown')
df['maidenName'] = df['maidenName'].fillna('Unknown')


# ===================== 2. Extract Useful Columns =====================
# Extract country and city from nested address columns
df['country'] = df['address.country']
df['city'] = df['address.city']


# ===================== 3. Standardize Text Data =====================
# Standardizing text avoids issues like Male / male / MALE
df['gender'] = df['gender'].str.lower().str.strip()
df['role'] = df['role'].str.lower().str.strip()
df['city'] = df['city'].str.title().str.strip()
df['country'] = df['country'].str.title().str.strip()


# ===================== 4. Remove Duplicate Records =====================
# Ensure each user appears only once (using email as unique identifier)
df.drop_duplicates(subset='email', inplace=True)


# ===================== 5. Feature Engineering - Age Groups =====================
# Create age categories for better demographic analysis
df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 25, 35, 50, 100],
    labels=['Young', 'Adult', 'Mid-Age', 'Senior']
)


# ===================== 6. Feature Engineering - Email Domain =====================
# Extract domain from email to analyze organization/provider distribution
df['email_domain'] = df['email'].str.split('@').str[1]


# ===================== 7. Derived Metric - BMI Calculation =====================
# Convert height from cm to meters
df['height_meter'] = df['height'] / 100

# Calculate Body Mass Index (BMI)
df['BMI'] = df['weight'] / (df['height_meter'] ** 2)


# ===================== 8. BMI Classification =====================
# Categorize users based on BMI health ranges
df['BMI_category'] = pd.cut(
    df['BMI'],
    bins=[0, 18.5, 25, 30, 100],
    labels=['Underweight', 'Normal', 'Overweight', 'Obese']
)


print("############# Cleaning & Transformation DONE ##########")


#--------------------------------  Analysis   --------------------------------

print("############# Analysis Started ! ##########")

#################### Average Age by role ######################
sns.set_style("whitegrid")
plt.figure(figsize=(5,6))
sns.barplot(data=df, 
            x='role', 
            y='age',
            hue='role',
            estimator='mean',
            palette='Set2',
            legend=False,
            errorbar=None
           
            )  

plt.title("Average Age by Role")
plt.xlabel("Role")
plt.ylabel("Average Age")
plt.tight_layout()
plt.savefig("plots/avg_age_by_role.png")
plt.close()


##################### Average Age by Gender ######################

sns.set_style("whitegrid")
plt.figure(figsize=(5,6))
sns.barplot(data=df, 
            x="gender", 
            y="age",
            hue='gender',
            estimator='mean',
            palette='Set2',
            legend=False,
            errorbar=None
           
            )  

plt.title("Average Age by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Age")
plt.tight_layout()
plt.savefig("plots/avg_age_by_gender.png")
plt.close()


##################### Number of users per Gender ######################
sns.set_style("whitegrid")
plt.figure(figsize=(5,6))
sns.countplot(data=df, 
            x="gender", 
            hue='gender',
            palette='Set2',

            )  

plt.title("Number of users per Gender")
plt.xlabel("Gender")
plt.ylabel("Number Of Users")
plt.tight_layout()
plt.savefig("plots/users_per_gender.png")
plt.close()


##################### Top 10 cities with the most users ######################
users_per_city=df['city'].value_counts().sort_values(ascending=False).reset_index()
users_per_city.columns=['city','user_count']

sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(data=users_per_city.head(10), 
            x="city", 
            y="user_count",
            hue='city',
            palette='Set2',

            )  

plt.title("Top 10 cities with the most users")
plt.xlabel("City")
plt.ylabel("Number Of Users")
plt.tight_layout()
plt.savefig("plots/top_cities.png")
plt.close()



##################### Average height colored by role ######################

sns.set_style("whitegrid")
sns.histplot(data=df, 
             x="height", 
             hue='role',
             multiple='stack',
             kde=True)   


plt.title(f"Average height={df['height'].mean():.2f} cm")
plt.xlabel("Height (cm)")
plt.ylabel("Number of users")
plt.tight_layout()
plt.savefig("plots/height_distribution.png")
plt.close()


##################### Average Weight colored by role ######################

sns.set_style("whitegrid")
sns.histplot(data=df, 
             x="weight", 
             hue='role',
             multiple='stack',
             kde=True)   

plt.title(f"Average Weight={df['weight'].mean():.2f} kg")
plt.xlabel("Weight (kg)")
plt.ylabel("Number of users")
plt.tight_layout()
plt.savefig("plots/weight_distribution.png")
plt.close()



##################### relationship between Age and height colored by gender ######################

sns.scatterplot(
        data=df, 
        x='age', 
        y='height', 
        hue='gender',
        )

plt.title("Relationship Between Age and Height")
plt.xlabel("Age")
plt.ylabel("Height (cm)")
plt.savefig("plots/age_vs_height.png")
plt.close()



##################### relationship between Age and weight colored by gender ######################

sns.scatterplot(
        data=df, 
        x='age', 
        y='weight', 
        hue='gender',
        )

plt.title("Relationship Between Age and Weight")
plt.xlabel("Age")
plt.ylabel("Weight (Kg)")
plt.savefig("plots/age_vs_weight.png")
plt.close()


print("############# Analysis DONE ! ##########")
print("############# plots are saved in plots directory #############")


