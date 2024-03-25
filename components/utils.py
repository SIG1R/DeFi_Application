import pandas as pd
import altair as alt

class graph_data:

    def __init__(self, *columns):
        '''
        Initialize a instance with one dataframe with the columns

        Arguments

        - columns: args of str names of the columns of your dataframe
        '''
        self.dataframe = pd.DataFrame(columns = columns)



    def add_row(self, row):
        '''
        Method that allow add a transaction (row) to you dataframe

        Arguments

        - row: this is a list with a elements of you new row.

        Examples:

        a) If you want add ONLY one transaction:
        
        b) If you want add multiples transactions:
        '''

#        assert type(row) == dict, 'row argument must be a dict type'

        # Adding row
        self.dataframe = pd.concat(
                [self.dataframe, row], # DataFrames to concat
                ignore_index = True # No replace index
        )


    def bar_chart(self, independent, dependent, title:str):
        '''
        Return altair config char, this method was think to implement
        at streamlit.

        Arguments

        - independent: name of a column of the independent variable.
        - dependent: name of a column of the dependent variable.
        '''

        assert type(title) == str, 'Title argument must be str type'

        config = alt.Chart(self.dataframe).mark_bar().encode(
            alt.Color(independent),
            x = independent,
            y = dependent
        ).properties(
            title = title
        )
        
        return config 

    def trend_chart(self, independent, dependent, color, title):
        '''
        '''
        assert type(title) == str, 'Title argument must be str type'
        
        # Create the base config chart
        base = alt.Chart(self.dataframe).encode(
            alt.Color(color).legend(None)
        ).properties(
            title = title
        )
        
        # Adding lines chart
        line = base.mark_line().encode(x=independent, y=dependent)
        
        # Adding the circle in last transaction
        last_price = base.mark_circle().encode(
            alt.X(f"last_date[{independent}]:T"),
            alt.Y(f"last_date[{dependent}]:Q")
            ).transform_aggregate(
                last_date=f"argmax({independent})",
                groupby=[color]
            )

        # Adding label of line chart
        company_name = last_price.mark_text(
                align="left",
                dx=4
        ).encode(text=color)

        config = (line + last_price + company_name).encode(
            x=alt.X().title(independent),
            y=alt.Y().title(dependent)
        )

        return config


