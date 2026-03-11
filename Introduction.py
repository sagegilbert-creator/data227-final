
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.title("GDP and Fertility Rate Analysis")
st.subheader("Project Question")
st.subheader("""What is the association between a country's Gross Domestic Product (GDP) and its Total Fertility Rate (TFR)? What can GDP tell us about a country's fertility rate?""")
st.markdown("""Our project aims to answer the above questions by analyzing associations in the United States, France, Japan, India, and Portugal. Fertility patterns vary substantially across countries due to differences in historical context, public policy, economic conditions, and cultural norms. Often, when interpreting fertility data, viewers may be inclined to rely on preconceived notions about a country and use them to make assumptions about why these patterns occur. By placing TFR alongside GDP growth, our goal is to disrupt those assumptions and evaluate whether economic indicators help explain changes in fertility over time.

The goal of this project is not to assume a causal relationship between GDP and fertility, but rather to examine whether consistent patterns emerge across different regional contexts. Even if economic growth ultimately proves to have little association with fertility changes, examining this relationship provides a useful starting point for understanding broader dynamics. Fertility trends affect families, labor markets, and populations worldwide, making their origins an important subject of study. We view our analysis as the starting point for a more comprehensive analytical project on those origins. 

Approaching the data through the question of what economic indicators can tell us about fertility patterns encourages non-trivial insights rather than simple description. By comparing multiple countries and examining both long-term trends and short-term changes, our analysis aims to generate meaningful insights into how economic conditions may relate to fertility change.""")
st.subheader("Data Collection")
st.markdown("""Our fertility data come from the Human Fertility Database (HFD), an open-access resource that provides comprehensive information on fertility across countries. We focus on data from the United States, France, Japan, India, and Portugal. Each country’s data are compiled by the HFD from a variety of sources, including national statistics offices, yearbooks, national health centers, and national registry data. In some cases, the data dates back to the early 1920s, although the exact dates vary by country. For the purposes of our analysis, we restricted all data to 1961-2022. GDP data for several countries are not available before 1961, and many fertility rates are not updated past 2022. Beyond that, using this 61-year range allows us to more closely examine fertility fluctuations in a broad historical context while maintaining consistent coverage across countries. (Note that, in our exploration, we allowed each country’s data to begin whenever the earliest observation was and go to its most recent observation, for purposes of exploration.)

The HFD dataset provides multiple fertility-related variables for each country. In total, fifteen variables are available. For our initial exploration, we used the total fertility rate, the age-specific fertility rate, and the mean age at birth. For our primary analysis, we focus on total fertility rate (TFR) and the number of births, as these measures provide a clear overview of fertility trends over time.
Because the HFD does not include data for India, we obtained India’s fertility data from the World Bank. We ensured that the World Bank measure of total fertility rate corresponds to the same definition used by the HFD (births per woman over a lifetime under current age-specific fertility rates). Similar to the HFD, the World Bank compiles its data from national statistical offices, demographic statistics, and the United Nations.
Our GDP data also comes from the World Bank. Specifically, we use GDP per capita growth (annual %) to best capture changes in a country’s economic conditions. While total GDP measures how large an economy is, fertility behavior is more likely to respond to changes in conditions than to the size of an economy. Therefore, GDP per capita growth is more suitable for this association. The World Bank collects its GDP data from national statistical offices and organizations, central banks, national accounts data files, and the Organization for Economic Cooperation and Development. 

We selected these five countries (the USA, France, Japan, India, and Portugal) because they represent diverse economic histories, cultural contexts, and policy environments that may influence both economic conditions and fertility patterns. While we acknowledge that this sample is insufficient to draw universal conclusions about the relationship between GDP and fertility worldwide, examining these cases allows us to explore how economic change and fertility trends may interact across different national contexts.

Our datasets were cleaned and standardized using pandas (mainly ensuring all “Year” values were the same object type), and fertility and GDP data were merged by country and year to enable direct comparison (into the dataframe named merged_all). To examine short-term dynamics, we calculated the annual change in the total fertility rate as the difference between consecutive years (charts #4). We also computed decade-level averages of GDP growth and fertility rates to highlight longer-term trends and reduce short-term variability (charts #2). All visualizations were produced using Python and the Altair visualization library, as we learned in class.
""")

st.header("Exploratory Fertility Patterns")
st.markdown("In order to familiarize ourselves with the data and its structure, we generated three types of visualizations for Japan, the USA, and France.")
st.subheader("Total Fertility Rates Over Time")
st.markdown("The below graphs are linked with a year selection. Hovering over a year on one graph will highlight the year on the other graphs with a dot, for easy comparison.")


# Loading Human Fertility Data
#TFR Data
jpn_tfr = pd.read_csv(
    "data/JPNtfrRR.txt",
    skiprows=2, delim_whitespace=True
)

jpn_tfr["Country"] = "Japan"

usa_tfr = pd.read_csv(
    "data/USAtfrRR.txt",
    skiprows=2, delim_whitespace=True
)

usa_tfr["Country"] = "USA"

fra_tfr = pd.read_csv(
    "data/FRATNPtfrRR.txt",
    skiprows=2, delim_whitespace=True
)

fra_tfr["Country"] = "France"


#TFR
def fix_year(df):
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["Year"]):
        df["Year"] = pd.to_datetime(df["Year"].astype(int).astype(str), format="%Y")
    df["YearNum"] = df["Year"].dt.year
    return df

jpn_tfr = fix_year(jpn_tfr)
usa_tfr = fix_year(usa_tfr)
fra_tfr = fix_year(fra_tfr)

year_sel = alt.selection_point(
    name="year_hover",
    fields=["YearNum"],
    on="mouseover",
    nearest=True,
    empty=False,
    clear="mouseout"
)

def make_chart(df, title):
    line = alt.Chart(df).mark_line().encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y=alt.Y("TFR:Q", title="Total Fertility Rate (TFR)"),
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0.2))
    )

    points = alt.Chart(df).mark_circle(size=80).encode(
        x=alt.X("Year:T"),
        y=alt.Y("TFR:Q"),
        tooltip=[
            alt.Tooltip("YearNum:Q", title="Year"),
            alt.Tooltip("TFR:Q", title="TFR", format=".2f")
        ],
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0))
    )

    return (line + points).properties(
        width=300,
        height=300,
        title=title
    )

jpn_tfr_line = make_chart(jpn_tfr, "Japan")
usa_tfr_line = make_chart(usa_tfr, "USA")
fra_tfr_line = make_chart(fra_tfr, "France")

linked_tfr = alt.hconcat(
    jpn_tfr_line,
    usa_tfr_line,
    fra_tfr_line
).add_params(year_sel)

st.altair_chart(linked_tfr, use_container_width=True)

st.caption("""
Figure 1 (Japan): This graph shows the change in Japan’s total fertility rate from 1947 to 2024. The overall trend is strongly downward. Fertility declines rapidly after the late 1940s, falling from approximately 4.3 children per woman in 1949 to 2.08 by 1957. A sharp drop occurs again in 1966, when fertility falls to roughly 1.6 children per woman. This decline may be associated with the cultural superstition of the “Fire-Horse” year, which discouraged births during that year. Fertility briefly increased in 1967 before continuing a gradual long-term decline with minor fluctuations, eventually reaching low levels in recent decades.

Figure 2 (United States): This graph shows the change in the United States’ total fertility rate from 1933 to 2023. The overall trend initially increases, peaking in 1957 at approximately 3.7 children per woman during the post–World War II “Baby Boom.” Following this peak, fertility declines sharply over the next two decades. After the late 1970s, fertility stabilized with moderate fluctuations before gradually declining again in recent years, reaching approximately 1.6 children per woman in 2023. These long-term changes correspond with broader social and economic shifts, including increased female labor force participation and a changing cultural perspective on family patterns.

Figure 3 (France): This graph shows the change in France’s total fertility rate from 1946 to 2022. Overall, the total fertility rate gradually declines over time with minor fluctuations, but it consistently remains above 1.5 children per woman. Fertility peaks in 1947 at approximately 3.03 children per woman before beginning a long-term decline. One of the most noticeable decreases occurs between 1970 and 1976, when the total fertility rate falls by about 0.1 children per woman.
""")


#ASFR data
jpn_asfr = pd.read_csv(
    "data/JPNasfrRR.txt",
    sep=r"\s+",
    skiprows=2,
    engine="python"
)

jpn_asfr["Age"] = jpn_asfr["Age"].astype(str).str.replace(r"[+-]", "", regex=True)
jpn_asfr["Country"] = "Japan"

usa_asfr = pd.read_csv(
    "data/USAasfrRR.txt",
    sep=r"\s+",
    skiprows=2,
    engine="python"
)
usa_asfr["Age"] = usa_asfr["Age"].astype(str).str.replace(r"[+-]", "", regex=True)
usa_asfr["Country"] = "USA"

fra_asfr = pd.read_csv(
    "data/FRATNPasfrRR.txt",
    sep=r"\s+",
    skiprows=2,
    engine="python"
)
fra_asfr["Age"] = fra_asfr["Age"].astype(str).str.replace(r"[+-]", "", regex=True)
fra_asfr["Country"] = "France"

#MAB data
jpn_mab = pd.read_csv(
    "data/JPNmabRR.txt",
    skiprows=2
)
jpn_mab["Country"] = "Japan"

usa_mab = pd.read_csv(
    "data/USAmabRR.txt",
    skiprows=2
)
usa_mab["Country"] = "USA"


fra_mab = pd.read_csv(
    "data/FRATNPmabRR.txt",
    skiprows=2
)
fra_mab["Country"] = "France"


# ASFR

st.subheader("Age-Specific Fertility Rate by Decade")
st.markdown("""Age-specific fertility rates (ASFR) are shown in the line graphs below and are averaged within the selected decade. Each panel displays the distribution of fertility by age for one country, while the decade selectors allow comparison of how these distributions change over time. In the earliest decades shown, the three countries reflect relatively similar fertility patterns, with peak fertility occurring between ages 23 and 26. Japan initially has the highest fertility rates, with a peak of approximately 0.20 children per woman at age 26. During the 1960s, Japan’s fertility distribution narrows considerably and remains narrower than those of the other countries until the 2000s. In the United States, fertility begins to shift toward older ages by the 1990s, reflecting a gradual postponement of childbearing. These patterns illustrate how fertility change can reflect shifts in the timing of childbearing, rather than only changes in the total number of births.""")

usa_asfr["Decade"] = ((usa_asfr["Year"] // 10) * 10).astype(int)

decades = sorted(usa_asfr["Decade"].unique().tolist())
decade_dropdown = alt.binding_select(options=decades, name="USA Decade: ")
decade_sel = alt.selection_point(
    fields=["Decade"],
    bind=decade_dropdown,
    value=[{"Decade": decades[0]}]
)

usa_asfr_chart = (
    alt.Chart(usa_asfr)
    .add_params(decade_sel)
    .transform_filter(decade_sel)
    .transform_aggregate(
        mean_ASFR="mean(ASFR)", groupby=["Age", "Decade"]
    )
    .mark_line(interpolate="monotone", strokeWidth=4)
    .encode(
        x=alt.X("Age:Q", title="Age"),
        y=alt.Y("mean_ASFR:Q", title="Average Age-Specific Fertility Rate"),
        tooltip=[alt.Tooltip("Decade:N"), alt.Tooltip("Age:Q"), alt.Tooltip("mean_ASFR:Q", format=".4f")]
    )
    .properties(
        title="USA",
        width=500,
        height=300
    )
)

jpn_asfr["Decade"] = ((jpn_asfr["Year"] // 10) * 10).astype(int)

decades = sorted(jpn_asfr["Decade"].unique().tolist())
decade_dropdown = alt.binding_select(options=decades, name="Japan Decade: ")
decade_sel = alt.selection_point(
    fields=["Decade"],
    bind=decade_dropdown,
    value=[{"Decade": decades[0]}]
)

jpn_asfr_chart = (
    alt.Chart(jpn_asfr)
    .add_params(decade_sel)
    .transform_filter(decade_sel)
    .transform_aggregate(
        mean_ASFR="mean(ASFR)", groupby=["Age", "Decade"]
    )
    .mark_line(interpolate="monotone", strokeWidth=4)
    .encode(
        x=alt.X("Age:Q", title="Age"),
        y=alt.Y("mean_ASFR:Q", title="Average Age-Specific Fertility Rate"),
        tooltip=[alt.Tooltip("Decade:N"), alt.Tooltip("Age:Q"), alt.Tooltip("mean_ASFR:Q", format=".4f")]
    )
    .properties(
        title="Japan",
        width=500,
        height=300
    )
)


fra_asfr["Decade"] = ((fra_asfr["Year"] // 10) * 10).astype(int)

decades = sorted(fra_asfr["Decade"].unique().tolist())
decade_dropdown = alt.binding_select(options=decades, name="France Decade: ")
decade_sel = alt.selection_point(
    fields=["Decade"],
    bind=decade_dropdown,
    value=[{"Decade": decades[0]}]
)

fra_asfr_chart = (
    alt.Chart(fra_asfr)
    .add_params(decade_sel)
    .transform_filter(decade_sel)
    .transform_aggregate(
        mean_ASFR="mean(ASFR)", groupby=["Age", "Decade"]
    )
    .mark_line(interpolate="monotone", strokeWidth=4)
    .encode(
        x=alt.X("Age:Q", title="Age"),
        y=alt.Y("mean_ASFR:Q", title="Average Age-Specific Fertility Rate"),
        tooltip=[alt.Tooltip("Decade:N"), alt.Tooltip("Age:Q"), alt.Tooltip("mean_ASFR:Q", format=".4f")]
    )
    .properties(
        title="France",
        width=500,
        height=300
    )
)

st.altair_chart(usa_asfr_chart, use_container_width=True)
st.altair_chart(jpn_asfr_chart, use_container_width=True)
st.altair_chart(fra_asfr_chart, use_container_width=True)

st.subheader("Mean Ages at Birth Over Time")
st.markdown("The below graphs are linked with a year selection. Hovering over a year on one graph will highlight the year on the other graphs with a dot, for easy comparison.")

# had to reload MAB files too idk why its being weird
usa_mab = pd.read_csv(
    "data/USAmabRR.txt",
    sep=r"\s+",
    skiprows=2,
    engine="python"
)
usa_mab["Country"] = "USA"

fra_mab = pd.read_csv(
    "data/FRATNPmabRR.txt",
    sep=r"\s+",
    skiprows=2,
    engine="python"
)
fra_mab["Country"] = "France"


jpn_mab = pd.read_csv(
    "data/JPNmabRR.txt",
    sep=r"\s+",
    skiprows=2,
    engine="python"
)
jpn_mab["Country"] = "Japan"

year_sel = alt.selection_point(
    encodings=["x"],
    on="mouseover",
    nearest=True,
    empty=False,
    clear="mouseout",
    name="yr"
)

usa_mab["Year"] = pd.to_datetime(usa_mab["Year"], format="%Y")

usa_mab_line = (
    alt.Chart(usa_mab).mark_line().encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y=alt.Y("MAB:Q", title="Mean Age at Birth (years)"),
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0.15))
    )
    +
    alt.Chart(usa_mab).mark_circle(size=80).encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y="MAB:Q",
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0))
    )
    +
    alt.Chart(usa_mab).mark_point().encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y="MAB:Q",
        opacity=alt.value(0),
        tooltip=[alt.Tooltip("Year:T"), alt.Tooltip("MAB:Q", format=".2f")]
    ).add_params(year_sel)
).properties(width=500, height=300, title="USA")

jpn_mab["Year"] = pd.to_datetime(jpn_mab["Year"], format="%Y")

jpn_mab_line = (
    alt.Chart(jpn_mab).mark_line().encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y=alt.Y("MAB:Q", title="Mean Age at Birth (years)"),
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0.15))
    )
    +
    alt.Chart(jpn_mab).mark_circle(size=80).encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y="MAB:Q",
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0))
    )
    +
    alt.Chart(jpn_mab).mark_point().encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y="MAB:Q",
        opacity=alt.value(0),
        tooltip=[alt.Tooltip("Year:T"), alt.Tooltip("MAB:Q", format=".2f")]
    ).add_params(year_sel)
).properties(width=500, height=300, title="Japan")

fra_mab["Year"] = pd.to_datetime(fra_mab["Year"], format="%Y")

fra_mab_line = (
    alt.Chart(fra_mab).mark_line().encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y=alt.Y("MAB:Q", title="Mean Age at Birth (years)"),
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0.15))
    )
    +
    alt.Chart(fra_mab).mark_circle(size=80).encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y="MAB:Q",
        opacity=alt.condition(year_sel, alt.value(1), alt.value(0))
    )
    +
    alt.Chart(fra_mab).mark_point().encode(
        x=alt.X("Year:T", axis=alt.Axis(format="%Y")),
        y="MAB:Q",
        opacity=alt.value(0),
        tooltip=[alt.Tooltip("Year:T"), alt.Tooltip("MAB:Q", format=".2f")]
    ).add_params(year_sel)
).properties(width=500, height=300, title="France")

linked_mab = (usa_mab_line & jpn_mab_line & fra_mab_line)
st.altair_chart(linked_mab, use_container_width=True)

st.caption("""
Figure 1 (United States):  This graph shows the change in the United States’ mean age of mothers at birth from 1933 to 2023. The overall trend increases over time. The mean age briefly peaks in 1945 at 27.74 years before gradually declining, reaching a low of 25.75 years in 1966. Since then, the mean age has steadily risen, reaching 29.96 years in 2023. This upward trend reflects broader social and demographic shifts that have contributed to later childbearing in the United States.

Figure 2 (Japan): This graph shows the change in Japan’s mean age of mothers at birth from 1947 to 2024. Initially, the mean age declines gradually, reaching a low of 27.64 years in 1973. After this point, the trend reverses and the age increases steadily, reaching 32.06 years in 2024. Japan’s mean age remains consistently higher than that of the United States, never falling below 27 years, suggesting differences in social norms and patterns surrounding childbearing.

Figure 3 (France):  This graph shows the change in France’s mean age of mothers at birth from 1946 to 2022. Compared with the other countries, France exhibits a relatively steady pattern. The mean age declines slightly until 1977, reaching 26.52 years, before beginning a gradual and consistent increase. By 2022, the mean age rises to 31.08 years, reflecting a long-term shift toward later childbearing.
""")
