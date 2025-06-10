import matplotlib.pyplot as plt
from IVtws import IVstream
import pandas as pd

def main():
    """
    Main function to run the IVtws stream, fetch data, and plot results.
    """
    print("Initializing IV stream...")
    # Opening and closing times for the market
    iv_stream = IVstream(opet=(8, 45), clost=(13, 45))

    try:
        print("Initializing data table...")
        # select_settled=0 corresponds to the weekly option
        iv_stream.init_table(select_settled=0)

        print("Fetching and appending IV data...")
        iv_stream.append_IV()

        # Set pandas display options to see all columns
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 200)

        print("\n--- Call Options ---")
        if not iv_stream.Call.empty:
            print(iv_stream.Call.head())
        else:
            print("No Call option data available.")

        print("\n--- Put Options ---")
        if not iv_stream.Put.empty:
            print(iv_stream.Put.head())
        else:
            print("No Put option data available.")

        # Plotting the results
        if not iv_stream.Call.empty and not iv_stream.Put.empty:
            print("\nPlotting Implied Volatility Smile...")
            fig, ax = plt.subplots(figsize=(13, 6))

            # Filter out deep in-the-money options for a clearer plot
            call_data = iv_stream.Call[iv_stream.Call['內含價值'] < 450].set_index('履約價', drop=False)
            put_data = iv_stream.Put[iv_stream.Put['內含價值'] < 450].set_index('履約價', drop=False)

            if not call_data.empty:
                call_data['隱含波動率'].plot(ax=ax, c='r', label='Call IV', marker='o')
            if not put_data.empty:
                put_data['隱含波動率'].plot(ax=ax, c='g', label='Put IV', marker='o')
            
            ax.set_title('Implied Volatility Smile')
            ax.set_xlabel('Strike Price (履約價)')
            ax.set_ylabel('Implied Volatility (隱含波動率)')
            ax.legend()
            ax.grid(True)
            plt.show()
        else:
            print("Cannot plot, not enough data.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing Selenium driver...")
        iv_stream.close_PhantomJS()
        print("Done.")


if __name__ == "__main__":
    main()