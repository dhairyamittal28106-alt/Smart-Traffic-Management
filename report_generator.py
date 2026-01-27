import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def generate_analytics_dashboard():
    try:
        # Load the data logged by main.py
        df = pd.read_csv('traffic_report.csv')
        
        if df.empty:
            print("Error: The CSV file is empty. Run main.py for a few minutes first.")
            return

        # Set the aesthetic style for a professional report
        sns.set_theme(style="darkgrid")
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
        fig.suptitle(f'Smart City Traffic Analytics Report\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', fontsize=16)

        # 1. Traffic Load & Queue Length Analysis
        ax1.fill_between(df['Timestamp'], df['Vehicles'], color="skyblue", alpha=0.4)
        ax1.plot(df['Timestamp'], df['Vehicles'], color="blue", linewidth=2, label='Vehicle Load')
        ax1.set_ylabel('Vehicle Count')
        ax1.set_title('Real-time Traffic Density & Congestion')
        ax1.legend(loc='upper left')

        # 2. Environmental Impact (CO2 Emissions)
        # This highlights how idling at red lights increases the carbon footprint
        ax2.plot(df['Timestamp'], df['CO2_Grams'], color="green", linewidth=2, label='CO2 Output (g/s)')
        ax2.fill_between(df['Timestamp'], df['CO2_Grams'], color="green", alpha=0.2)
        ax2.set_ylabel('Grams of CO2')
        ax2.set_title('Environmental Impact Assessment')
        ax2.legend(loc='upper left')

        # 3. Pedestrian & Safety Activity
        # Monitors vulnerable road users to justify safety-based signal timing
        ax3.bar(df['Timestamp'], df['Pedestrians'], color="magenta", alpha=0.6, label='Pedestrians Detected')
        ax3.set_ylabel('Count')
        ax3.set_xlabel('Time (HH:MM:SS)')
        ax3.set_title('Pedestrian Activity & Safety Monitoring')
        ax3.legend(loc='upper left')

        # Rotate timestamps for better readability
        plt.xticks(rotation=45)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Save the final report image
        output_file = 'traffic_analytics_report.png'
        plt.savefig(output_file, dpi=300)
        print(f"Success! Dashboard saved as: {output_file}")
        
        # Display the window
        plt.show()

    except FileNotFoundError:
        print("Error: 'traffic_report.csv' not found. Ensure main.py has run successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    generate_analytics_dashboard()