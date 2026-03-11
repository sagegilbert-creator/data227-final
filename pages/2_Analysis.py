
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout="wide")

st.title("Analysis: The Association between GDP and TFR")
st.markdown("""To bolster the narrative of our analysis, we generated four types of visualizations: a multi-line time series, a decade-level GDP bar and TFR line, a bubble chart, and an annual change bar chart. These are appropriate for our analysis because each visualization highlights a different dimension of the data. The multi-line time series provides a broad overview of long-term trends within and across countries, allowing us to situate fertility changes within their historical economic context. The decade-level GDP bar and TFR line summarize these patterns by smoothing short-term fluctuations and emphasizing structural shifts over time. The bubble chart then visualizes the direct relationship between GDP and total fertility rates across decade-level observations, helping reveal potential correlations and cross-country clustering. Finally, the annual change bar chart focuses on short-term dynamics, illustrating whether year-to-year economic fluctuations are associated with changes in fertility. Taken together, these visualizations allow us to move from descriptive trends to more focused examinations of potential relationships between economic conditions and fertility behavior.""")

st.subheader("Multi-Line TFR & GDP Over Time")
st.markdown("""This multi-line chart compares changes in fertility rates and economic growth over time for France, India, Japan, Portugal, and the United States. In the visualization, solid lines represent the Total Fertility Rate (TFR), while dashed lines represent GDP, with the left axis measuring fertility rate and the right axis measuring GDP. A dropdown allows viewers to display TFR, GDP, or both metrics to better observe how demographic and economic trends evolve.

The overall goal of this graph is to examine how fertility rates change over time alongside economic development in various countries. By plotting both variables on the same timeline, we can determine whether increases in economic output tend to coincide with declines in fertility rates, a pattern often associated with demographic transition. According to the National Bureau of Economic Research, rapid economic growth in the face of persistent traditional gender roles can result in fertility declines, particularly when women remain responsible for the majority of unpaid domestic labor.""")

#GDP per capita growth data (annual %)
#recessions = - values

gdp = pd.read_csv(
    "data/GDP.csv", skiprows=4)

gdp = gdp[gdp["Country Name"].isin(["United States", "France", "Japan", "Portugal", "India"])]
gdp = gdp.drop(columns =["1960" , "Country Code" , "Indicator Name" , "Indicator Code", "2023", "2024", "2025", "Unnamed: 70"])

prt_tfr = pd.read_csv(
    "data/PRTtfrRR.txt",
    skiprows=2, delim_whitespace=True)

prt_tfr["Country"] = "Portugal"

ind_tfr = pd.read_csv("data/WBIndtfr.csv", skiprows=4)

ind_tfr = ind_tfr[ind_tfr["Country Name"] == "India"]

ind_tfr = ind_tfr.drop(columns = ["Country Code" , "Indicator Name", "Indicator Code" , "1960" , "2023" , "2024" , "2025", "Unnamed: 70"])

ind_tfr = ind_tfr.melt(
    id_vars="Country Name",
    var_name="Year",
    value_name="TFR")

ind_tfr = ind_tfr.rename(columns={"Country Name": "Country"})


gdp_long = gdp.melt(
    id_vars="Country Name",
    var_name="Year",
    value_name="GDP")

gdp_long = gdp_long.rename(columns={"Country Name": "Country"})

gdp_long["Year"] = pd.to_numeric(gdp_long["Year"], errors="coerce")
gdp_long["GDP"] = pd.to_numeric(gdp_long["GDP"], errors="coerce")

gdp_long = gdp_long.dropna(subset=["Year", "GDP"])
gdp_long["Year"] = gdp_long["Year"].astype(int)

usa_tfr2 = pd.read_csv(
    "data/USAtfrRR.txt",
    skiprows=2, delim_whitespace=True
)

usa_tfr2["Country"] = "USA"

jpn_tfr2 = pd.read_csv(
    "data/JPNtfrRR.txt",
    skiprows=2, delim_whitespace=True
)

jpn_tfr2["Country"] = "Japan"

fra_tfr2 = pd.read_csv(
    "data/FRATNPtfrRR.txt",
    skiprows=2, delim_whitespace=True
)

fra_tfr2["Country"] = "France"

#shaping usa tfr
usa_tfr2 = usa_tfr2.copy()
usa_tfr2 = usa_tfr2[usa_tfr2["Year"] >= 1961]
usa_tfr2 = usa_tfr2[usa_tfr2["Year"] <= 2022]
usa_tfr2["Country"] = "United States"
usa_tfr2 = usa_tfr2[["Year", "TFR", "Country"]].copy()

usa_gdp = gdp_long[gdp_long["Country"] == "United States"].copy()
usa_merged = pd.merge(
    usa_tfr2,
    usa_gdp,
    on=["Country", "Year"],
    how="inner")

usa_merged["Decade"] = (usa_merged["Year"] // 10) * 10
usa_decade = (
    usa_merged.groupby(["Country", "Decade"], as_index=False)
    .agg(avg_TFR=("TFR", "mean"),
        avg_GDP=("GDP", "mean")))

decade_sel = alt.selection_point(fields=["Decade"], empty="all")

gdp_barusa = (
    alt.Chart(usa_decade)
    .mark_bar(opacity=0.75)
    .add_params(decade_sel)   # ← ADD THIS
    .encode(
        x=alt.X("Decade:O", title="Decade"),
        y=alt.Y(
            "avg_GDP:Q",
            title="Average GDP per Capita Growth (%)",
            axis=alt.Axis(titleColor="light blue")
        ),
        opacity=alt.condition(decade_sel, alt.value(1), alt.value(0.35)),
        tooltip=[
            alt.Tooltip("Decade:O", title="Decade"),
            alt.Tooltip("avg_GDP:Q", title="Avg GDP Growth", format=".2f"),
            alt.Tooltip("avg_TFR:Q", title="Avg TFR", format=".2f"),
        ],
    )
)

tfr_lineusa = (
    alt.Chart(usa_decade).mark_line(point=alt.OverlayMarkDef(size=80, color = "pink"), color = "pink")
    .encode(
        x=alt.X("Decade:O"),
        y=alt.Y(
            "avg_TFR:Q",
            title="Average TFR",
            axis=alt.Axis(titleColor="pink"))))

usa_dual_axis = (
    alt.layer(gdp_barusa, tfr_lineusa)
    .resolve_scale(y="independent")
    .properties(
        title="United States: Average TFR and GDP Growth by Decade",
        width=300,
        height=200))

fra_tfr2 = fra_tfr2[["Year", "TFR"]].copy()
fra_tfr2["Country"] = "France"
fra_tfr2 = fra_tfr2[fra_tfr2["Year"] >= 1961]
fra_tfr2 = fra_tfr2[fra_tfr2["Year"] <= 2022]
fra_tfr2 = fra_tfr2[["Year", "TFR", "Country"]].copy()

jpn_tfr2 = jpn_tfr2[["Year", "TFR"]].copy()
jpn_tfr2["Country"] = "Japan"
jpn_tfr2 = jpn_tfr2[jpn_tfr2["Year"] >= 1961]
jpn_tfr2 = jpn_tfr2[jpn_tfr2["Year"] <= 2022]
jpn_tfr2 = jpn_tfr2[["Year", "TFR", "Country"]].copy()

prt_tfr = prt_tfr[["Year", "TFR"]].copy()
prt_tfr["Country"] = "Portugal"
prt_tfr = prt_tfr[prt_tfr["Year"] >= 1961]
prt_tfr = prt_tfr[prt_tfr["Year"] <= 2022]
prt_tfr = prt_tfr[["Year", "TFR", "Country"]].copy()

#df for all of them for comparison
tfr_all = pd.concat(
    [usa_tfr2, fra_tfr2, jpn_tfr2, prt_tfr, ind_tfr],
    ignore_index=True)

tfr_all["Year"] = pd.to_numeric(tfr_all["Year"], errors="coerce")
gdp_long["Year"] = pd.to_numeric(gdp_long["Year"], errors="coerce")

merged_all = pd.merge(
    tfr_all,
    gdp_long,
    on=["Country", "Year"],
    how="inner")

dual_axis_df = merged_all.copy()

dual_axis_df["Year"] = pd.to_numeric(dual_axis_df["Year"], errors="coerce").round().astype("Int64")
dual_axis_df["TFR"] = pd.to_numeric(dual_axis_df["TFR"], errors="coerce")
dual_axis_df["GDP"] = pd.to_numeric(dual_axis_df["GDP"], errors="coerce")

dual_axis_df = dual_axis_df.dropna(subset=["Year", "TFR", "GDP", "Country"]).copy()
dual_axis_df["Year"] = dual_axis_df["Year"].astype(int)

# Legend click selection for countries
country_select = alt.selection_point(
    fields=["Country"],
    bind="legend",
    on="click"
)

# Dropdown for metric view
metric_dropdown = alt.binding_select(
    options=["Both", "TFR only", "GDP only"],
    name="Select Metric: "
)

metric_select = alt.param(
    name="MetricSelect",
    bind=metric_dropdown,
    value="Both"
)

base = (
    alt.Chart(dual_axis_df)
    .add_params(country_select, metric_select)
    .encode(
        x=alt.X(
            "Year:Q",
            title="Year",
            axis=alt.Axis(format="d", tickCount=10)
        ),
        color=alt.Color("Country:N", title="Country"),
        opacity=alt.condition(country_select, alt.value(1), alt.value(0.15)),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("Year:Q", title="Year", format="d"),
            alt.Tooltip("TFR:Q", title="Total Fertility Rate", format=".2f"),
            alt.Tooltip("GDP:Q", title="GDP", format=",.2f")
        ]
    )
)

# TFR layer
tfr_lines = (
    base.mark_line()
    .transform_filter(
        (metric_select == "Both") | (metric_select == "TFR only")
    )
    .encode(
        y=alt.Y(
            "TFR:Q",
            title="Total Fertility Rate (TFR)"
        ),
        size=alt.condition(country_select, alt.value(4), alt.value(1))
    )
)

# GDP layer
gdp_lines = (
    base.mark_line(strokeDash=[6, 4])
    .transform_filter(
        (metric_select == "Both") | (metric_select == "GDP only")
    )
    .encode(
        y=alt.Y(
            "GDP:Q",
            title="GDP",
            axis=alt.Axis(orient="right")
        ),
        size=alt.condition(country_select, alt.value(3), alt.value(1.5))
    )
)

fertility_gdp_dual_axis_interactive = (
    alt.layer(tfr_lines, gdp_lines)
    .resolve_scale(y="independent")
    .properties(
        width=850,
        height=500
    )
)

st.altair_chart(fertility_gdp_dual_axis_interactive, use_container_width=True)
st.caption("Total Fertility Rate (solid lines) and GDP trends (dashed lines) by country from 1961–2022")
st.markdown("""From the line graph, we can visualize how the numerical variables in our data change over time. Across most countries, the total fertility rate (depicted by solid lines) shows a long-term decreasing trend. India shows the most rapid decline, falling from almost 6 children per woman in the early 1960s to around 2 by the 2010s. France declines more gradually, stabilizing between 1.7 and 2.0 children per woman, and remaining as the developed country with the highest fertility rate in the visualization. The United States also follows the trend of the other countries, declining from a fertility rate of 3.5 in the 1960s to just below 2.0 in the 2000s. Japan and Portugal followed similar trends, falling from around 2 to 2.5 children per woman in the 1960s to near 1.5 over the last few decades. Overall, we see that fertility rates are declining over time, with developed countries following a similar trend. 

The GDP trends (indicated by the dashed lines) represent the annual growth rates per country, resulting in large year-to-year fluctuations. We see frequent, rapid spikes and drops that reflect economic expansions and recessions of each country, with growth rates fluctuating mainly around positive values. However, during periods of economic downturn, the GDP growth rate falls below zero. The data is much more volatile than fertility rates. Several countries experienced sharp drops during periods of global economic disruptions, which we discuss in our analysis. Overall, the GDP growth shows high variability over time, unlike the steady long-term decline observed in the fertility rate.

Taking these two variables together, we noticed key contrasts between them. The fertility rate lines decline mostly gradually over time, showing smooth downward trends across the countries. This pattern indicates that fertility decisions change slowly as societies develop, which could reflect shifts in education, urbanization, labor, and family planning. In contrast, the dashed GFP growth lines fluctuate much more substantially from year to year. We see that economic growth rates frequently rise and fall, reflecting business cycles, economic booms and recessions, and global patterns. These fluctuations tend to occur much more rapidly than changes in fertility rates, speaking to the volatility and unpredictability of a country's GDP. 

The main insight from this visualization is that fertility rates across countries show a long-term decline while GDP growth rates have significant short-term variability. Demographic indicators, such as fertility rates, tend to evolve more gradually over time, reflecting long-term social transitions, whereas economic growth trends respond immediately to changing conditions. Despite the volatility of GDP growth, the overall pattern suggests that long-term economic development is associated with declining fertility. This pattern is consistent with the theory of demographic transition, in which improvements in economic conditions, access to healthcare, and education all contribute to smaller family sizes.""")

st.subheader("Focused Summary: Average TFR and GDR Growth by Decade, per Country")
st.markdown("""These figures summarize long-term relationships between economic growth and fertility across the United States, France, Japan, India, and Portugal from 1961-2022. Bars represent average GDP per capita growth by decade, while lines represent average total fertility rates (TFR). By aggregating annual data into decades, the visualization highlights structural trends rather than short-term fluctuations. Comparing countries within the same framework allows for examination of whether periods of economic expansion correspond with shifts in fertility behavior across different economic and demographic contexts.

Use the dropdown below to select a decade. The selected decade is highlighted in each country panel and used to populate the cross-country comparison charts.
""")

# --- Build decade-level data correctly ---
merged_alldecs = merged_all.copy()
merged_alldecs["Decade"] = (merged_alldecs["Year"] // 10) * 10

decade_all = (
    merged_alldecs.groupby(["Country", "Decade"], as_index=False)
    .agg(
        avg_TFR=("TFR", "mean"),
        avg_GDP=("GDP", "mean")
    )
)

# --- Shared Streamlit control ---
decades = sorted(decade_all["Decade"].dropna().unique().tolist())
selected_decade = st.selectbox("Select decade", decades, index=0)

# --- Country colors ---
country_colors = {
    "United States": "pink",
    "France": "orange",
    "Japan": "navy",
    "Portugal": "green",
    "India": "red"
}

# --- Helper function to build each country panel ---
def make_country_dual_axis_chart(df, country, line_color):
    country_df = df[df["Country"] == country].copy()
    country_df["selected"] = country_df["Decade"] == selected_decade

    gdp_bar = (
        alt.Chart(country_df)
        .mark_bar(opacity=0.75)
        .encode(
            x=alt.X("Decade:O", title="Decade"),
            y=alt.Y(
                "avg_GDP:Q",
                title="Average GDP Growth (%)",
                axis=alt.Axis(titleColor="darkblue")
            ),
            opacity=alt.condition(
                alt.datum.selected,
                alt.value(1),
                alt.value(0.35)
            ),
            tooltip=[
                alt.Tooltip("Decade:O", title="Decade"),
                alt.Tooltip("avg_GDP:Q", title="Avg GDP Growth", format=".2f"),
                alt.Tooltip("avg_TFR:Q", title="Avg TFR", format=".2f")
            ]
        )
    )

    tfr_line = (
        alt.Chart(country_df)
        .mark_line(
            point=alt.OverlayMarkDef(size=80, color=line_color),
            color=line_color
        )
        .encode(
            x=alt.X("Decade:O", title="Decade"),
            y=alt.Y(
                "avg_TFR:Q",
                title="Average TFR",
                axis=alt.Axis(titleColor=line_color)
            ),
            tooltip=[
                alt.Tooltip("Decade:O", title="Decade"),
                alt.Tooltip("avg_TFR:Q", title="Avg TFR", format=".2f"),
                alt.Tooltip("avg_GDP:Q", title="Avg GDP Growth", format=".2f")
            ]
        )
    )

    return (
        alt.layer(gdp_bar, tfr_line)
        .resolve_scale(y="independent")
        .properties(
            title=country,
            width=300,
            height=220
        )
    )

# --- Build country charts ---
usa_dual_axis = make_country_dual_axis_chart(decade_all, "United States", "pink")
fra_dual_axis = make_country_dual_axis_chart(decade_all, "France", "orange")
jpn_dual_axis = make_country_dual_axis_chart(decade_all, "Japan", "navy")
ind_dual_axis = make_country_dual_axis_chart(decade_all, "India", "red")
prt_dual_axis = make_country_dual_axis_chart(decade_all, "Portugal", "green")

# --- Comparison charts for selected decade only ---
selected_df = decade_all[decade_all["Decade"] == selected_decade].copy()

compare_gdp = (
    alt.Chart(selected_df)
    .mark_bar()
    .encode(
        x=alt.X("Country:N", title="Country", sort="-y"),
        y=alt.Y("avg_GDP:Q", title="Average GDP per Capita Growth (%)"),
        color=alt.Color(
            "Country:N",
            scale=alt.Scale(
                domain=list(country_colors.keys()),
                range=list(country_colors.values())
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("Decade:O", title="Decade"),
            alt.Tooltip("avg_GDP:Q", title="Avg GDP Growth", format=".2f")
        ]
    )
    .properties(
        title=f"Selected Decade ({selected_decade}): Average GDP Growth Across Countries",
        width=320,
        height=300
    )
)

compare_tfr = (
    alt.Chart(selected_df)
    .mark_bar()
    .encode(
        x=alt.X("Country:N", title="Country", sort="-y"),
        y=alt.Y("avg_TFR:Q", title="Average TFR"),
        color=alt.Color(
            "Country:N",
            scale=alt.Scale(
                domain=list(country_colors.keys()),
                range=list(country_colors.values())
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("Decade:O", title="Decade"),
            alt.Tooltip("avg_TFR:Q", title="Avg TFR", format=".2f")
        ]
    )
    .properties(
        title=f"Selected Decade ({selected_decade}): Average TFR Across Countries",
        width=320,
        height=300
    )
)

# --- Render in rows ---
row1 = usa_dual_axis | fra_dual_axis | jpn_dual_axis
row2 = ind_dual_axis | prt_dual_axis
row3 = compare_gdp | compare_tfr

st.altair_chart(row1, use_container_width=True)
st.caption("""USA: In the United States, fertility declines steadily from the 1960s onward, while GDP growth fluctuates modestly across decades. The long-term decline in fertility following the post-World War II baby boom is highlighted, alongside a slight decline in GDP growth from the 2000s. That decline corresponds with 2008’s Great Recession. Despite this slight decline, the graph suggests that fertility decline occurs even during periods of continued economic expansion.

France: GDP growth declines gradually from the rapid expansion of the 1960s to slower growth in recent decades, while fertility falls modestly until the 1990s, but remains relatively stable compared to other developed countries. The visualization highlights France’s comparatively moderate fertility decline despite drastically slowing economic growth.

Japan: Japan experienced extremely rapid GDP growth in the 1960s, followed by a sustained slowdown, while fertility steadily declined across the decades. In the 1960s, Japan experienced what experts call an “economic miracle,” marked by rapid economic growth and stability post-World War II and throughout the Cold War. During this miracle, Japan’s GDP growth reached the highest level among the countries studied. An oil crisis in 1973 caused the beginning of a slowdown in Japan’s economy. The visualization emphasizes Japan’s pronounced fertility decline during and after its period of rapid economic development. Japan’s fertility rate largely mirrors its GDP growth rate, suggesting the country’s reliance on economic resources for childbearing.""")

st.altair_chart(row2, use_container_width=True)
st.caption("""India: Fertility declines consistently and sharply across decades while GDP growth accelerates, particularly after the 1980s and 1990s. The visualization highlights a simultaneous pattern of economic expansion and rapid fertility decline during India’s development period, and displays almost an inverse relationship between TFR and GDP growth. 

Portugal: Fertility falls steadily from higher levels in the 1960s to well below rates of 1.5 in recent decades, while GDP growth declines from rapid post-World War II expansion to slower modern growth. The visualization emphasizes Portugal’s transition toward low fertility during a period of economic maturation. Similar to Japan, Portugal’s fertility rate largely reflects its GDP growth, underscoring the association between the metrics. """)

st.altair_chart(row3, use_container_width=True)
st.caption("""These bar charts compare average GDP per capita growth and total fertility rates across the five countries for the selected decade. The comparison highlights substantial variation in economic growth and fertility across national contexts. India exhibits the highest growth and fertility levels, while developed economies such as Japan and Portugal display lower fertility despite more varied economic growth.""")

births_df = pd.read_csv(
     "Data/PRTbirthsRR.txt",
    sep=r"\s+",
    skiprows=1,
    header=1,
    na_values="."
)

births_df = births_df[["Year", "Age", "Total"]].copy()

births_df = births_df.rename(columns={"Total": "Births"})

births_df["Year"] = pd.to_numeric(births_df["Year"], errors="coerce")

births_df["Age"] = births_df["Age"].astype(str).str.replace(r"[^0-9]", "", regex=True)
births_df["Age"] = pd.to_numeric(births_df["Age"], errors="coerce")

births_df["Births"] = pd.to_numeric(births_df["Births"], errors="coerce")

births_df = births_df.dropna(subset=["Year", "Births"])

births_by_year = (
    births_df.groupby("Year", as_index=False)["Births"]
    .sum()
)

births_by_year["Country"] = "Portugal"

births_by_year.head()

def load_births(file, country):

    births_df = pd.read_csv(
        file,
        sep=r"\s+",
        skiprows=2,
        names=["Year", "Age", "Births"],
        usecols=[0,1,2],
        na_values="."
    )

    births_df["Year"] = pd.to_numeric(births_df["Year"], errors="coerce")
    births_df["Births"] = pd.to_numeric(births_df["Births"], errors="coerce")

    births_df["Age"] = births_df["Age"].astype(str).str.replace(r"[^0-9]", "", regex=True)
    births_df["Age"] = pd.to_numeric(births_df["Age"], errors="coerce")

    births_df = births_df.dropna(subset=["Year", "Births"])

    births_year = births_df.groupby("Year", as_index=False)["Births"].sum()

    births_year["Country"] = country
    births_year["Year"] = births_year["Year"].astype(int)

    return births_year
base = "data/"

fra_births = load_births(base + "FRATNPbirthsRR.txt", "France")
jpn_births = load_births(base + "JPNbirthsRR.txt", "Japan")
usa_births = load_births(base + "USAbirthsRR.txt", "United States")
prt_births = load_births(base + "PRTbirthsRR.txt", "Portugal")

births_all = pd.concat(
    [fra_births, jpn_births, usa_births, prt_births],
    ignore_index=True
    )

merged_all = merged_all.drop(
    columns=["Births", "Births_x", "Births_y"],
    errors="ignore"
)

merged_all = merged_all.merge(
    births_all,
    on=["Country", "Year"],
    how="left"
)
merged_all["Births"] = merged_all["Births"].round().astype("Int64")

bubble_df = merged_all.copy()

bubble_df["Year"] = pd.to_numeric(bubble_df["Year"], errors="coerce")
bubble_df["TFR"] = pd.to_numeric(bubble_df["TFR"], errors="coerce")
bubble_df["GDP"] = pd.to_numeric(bubble_df["GDP"], errors="coerce")
bubble_df["Births"] = pd.to_numeric(bubble_df["Births"], errors="coerce")

bubble_df = bubble_df.dropna(subset=["Country", "Year", "TFR", "GDP", "Births"]).copy()
bubble_df["Year"] = bubble_df["Year"].round().astype(int)
bubble_df["Decade"] = (bubble_df["Year"] // 10) * 10

decade_min = int(bubble_df["Decade"].min())
decade_max = int(bubble_df["Decade"].max())

decade_slider = alt.binding_range(
    min=decade_min,
    max=decade_max,
    step=10,
    name="Select Decade: "
)

decade_select = alt.param(
    name="DecadeSelect",
    bind=decade_slider,
    value=decade_min
)

base = (
    alt.Chart(bubble_df)
    .add_params(decade_select)
    .transform_filter(alt.datum.Decade == decade_select)
    .encode(
        x=alt.X(
        "GDP:Q",
        title="GDP per Capita",
        scale=alt.Scale(zero=False)
        ),
        y=alt.Y(
            "TFR:Q",
            title="Total Fertility Rate (TFR)"
        ),
        color=alt.Color(
            "Country:N",
            title="Country"
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("Year:Q", title="Year"),
            alt.Tooltip("GDP:Q", title="GDP", format=",.2f"),
            alt.Tooltip("TFR:Q", title="TFR", format=".2f"),
            alt.Tooltip("Births:Q", title="Number of Births", format=",.0f")
        ]
    )
)

decade_paths = base.mark_line(
    opacity=0.25,
    strokeWidth=1.5
).encode(
    detail="Country:N"
)

decade_points = base.mark_circle(
    opacity=0.7,
    stroke="black",
    strokeWidth=0.8
).encode(
    size=alt.Size(
    "Births:Q",
    title="Number of Births",
    scale=alt.Scale(
    type="sqrt",
    range=[20, 4500]),
    legend=alt.Legend(
        values=[200000, 500000, 1000000, 2000000, 3000000, 4000000],
        format=","
    )

    )

)


fertility_gdp_bubble_decade = (
    alt.layer(decade_paths, decade_points)
    .properties(
        width=850,
        height=550,
        title="GDP, Fertility, and Births by Country Across Decades"
    )
)

st.altair_chart(fertility_gdp_bubble_decade, use_container_width=True)
st.caption("Relationship between GDP per capita growth and TFR across countries and decades (from 1961-2022).")
st.markdown("""Analyzing the data by country, we see that across decades, France appears in the middle to upper range of GDP values, with fertility rates generally between 1.6 and 2.0 children per woman. For most decades, the data points for France are clustered fairly tightly, which indicates relatively stable fertility levels despite economic growth. Compared with over countries in the visualization, France also appears to have a slightly higher fertility rate.

The data for Japan show lower fertility rates across the decades compared to other countries, with earlier decades having total fertility rates around 1.8 and 2.2, and later decades with fertility rates closer to 1.3 and 1.6. Japan’s GDP per capita, however, remains clustered near the higher end, indicating strong economic development with low fertility rates.

Between the 1960s and 1990s, Portugal appeared to have one of the highest fertility rates among countries, ranging from 2.2 to 3.2. However, after the 1990s, this trend shifted, and Portugal had much lower fertility rates than Japan, France, and the United States. Portugal’s GDP per capita remains the most spread out across decades, with no clustering and a large dispersion of data points. This pattern suggests that economic development may not be associated with changes in fertility rates, as identifying a clear trend in this data is difficult. 

The United States appears to have a shift in GDP per capita across decades. In the 1960s and 1970s, the data were clustered to the left of the graph at lower GDP per capita values. Over time, we see this trend shift to the right, indicating growth in GDP per capita from the 1970s through the 2020s. In terms of fertility rate, in earlier decades, the United States had higher rates than other countries, ranging from 2.5 to 3.6. Over time, as GDP per capita increases, the fertility rate decreases, with the United States no longer the country with the highest fertility rate and instead falling somewhere in the middle, with variability across years. The bubbles for the United States are also noticeably larger than those for the other countries, due to the U.S.’s larger population and, therefore, a greater number of births. From the bubble size, we see how population size can influence total births even when total fertility rates are similar across countries.

Overall, the bar chart suggests that short-term economic fluctuations do not immediately affect fertility rates on a large scale. GDP growth fluctuates considerably more from year to year, but fertility rates tend to be closer together across years, with gradual changes across decades. 
""")

st.subheader("Annual GDP Growth and TFR Changes per Country")
st.markdown("""To examine whether short-term economic fluctuations correspond with changes in fertility behavior, we constructed a series of annual change bar charts for each country. By plotting annual GDP growth alongside annual changes in fertility, the visualization highlights short-term changes and any potential responsiveness of fertility to economic shocks. This approach allows us to evaluate whether increases or decreases in economic performance are associated with immediate or lagged shifts in fertility. Because annual fertility changes can occasionally produce extreme values, several unusually large TFR changes are clipped to maintain a consistent scale across countries; however, the underlying values remain available through tooltips. This visualization helps determine whether fertility appears to respond immediately, with delay, or not at all to fluctuations in economic conditions.""")

#India annual changes graph

inannydf = merged_all[merged_all["Country"] == "India"].copy()
inannydf = inannydf.sort_values("Year")
inannydf["TFR_change"] = inannydf["TFR"].diff()
inannydf = inannydf.dropna(subset=["GDP", "TFR_change"]).copy()
inannydf["Year"] = pd.to_numeric(inannydf["Year"], errors="coerce")
inannydf = inannydf.dropna(subset=["Year"])
inannydf["Year"] = inannydf["Year"].astype(int)

gdp_changeind= (
    alt.Chart(inannydf)
    .mark_bar(size=10, opacity=0.75)
    .encode(
        x=alt.X("Year:O",title="Year",axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
       y=alt.Y("GDP:Q",title="GDP Growth (%)",
            axis=alt.Axis(titleColor="teal", orient="left"),scale=alt.Scale(domain=[-10, 10]),),
        color=alt.value("teal"),
        tooltip=["Year", "GDP"]))

tfr_changeind = (
    alt.Chart(inannydf)
    .mark_bar(size=3, opacity=0.85)
    .encode(
        x=alt.X(
    "Year:O",
    title="Year",
    axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
        y=alt.Y(
            "TFR_change:Q",
            title="Annual TFR Change",
            axis=alt.Axis(titleColor="navy", orient="right"), scale=alt.Scale(domain=[-0.14, 0.14])
        ),color=alt.value("navy"),
        tooltip=["Year", "TFR_change"]))

zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="gray").encode(y="y:Q")

indchanges = (
    alt.layer(gdp_changeind, tfr_changeind, zero_line)
    .resolve_scale(y="independent")
    .properties(
        title="India: Annual GDP Growth and TFR Change",
        width=700,
        height=320))

st.altair_chart(indchanges, use_container_width=True)
st.caption("""India displays larger fluctuations in economic growth compared to the other countries in this study, particularly during periods of rapid economic expansion. At the same time, fertility changes remain largely negative, reflecting the country’s ongoing demographic transition toward lower fertility. While economic fluctuations occasionally coincide with shifts in fertility, the overall pattern suggests that fertility decline continues relatively independently of short-term economic variation. This indicates that broader demographic transitions and social changes may be the dominant drivers of fertility change in India.""")


#Portugal annual changes graph
prtannydf = merged_all[merged_all["Country"] == "Portugal"].copy()
prtannydf = prtannydf.sort_values("Year")
prtannydf["TFR_change"] = prtannydf["TFR"].diff()
prtannydf = prtannydf.dropna(subset=["GDP", "TFR_change"]).copy()
prtannydf["Year"] = pd.to_numeric(prtannydf["Year"], errors="coerce")
prtannydf = prtannydf.dropna(subset=["Year"])
prtannydf["Year"] = prtannydf["Year"].astype(int)

gdp_changeprt= (
    alt.Chart(prtannydf)
    .mark_bar(size=10, opacity=0.75)
    .encode(
        x=alt.X("Year:O",title="Year",axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
       y=alt.Y("GDP:Q",title="GDP Growth (%)",
            axis=alt.Axis(titleColor="teal", orient="left"),scale=alt.Scale(domain=[-10, 10]),),
        color=alt.value("teal"),
        tooltip=["Year", "GDP"]))

#for the extreme TFR values
prtannydf["TFR_change_plot"] = prtannydf["TFR_change"].clip(-0.14, 0.14)

tfr_changeprt = (
    alt.Chart(prtannydf)
    .mark_bar(size=3, opacity=0.85)
    .encode(
        x=alt.X(
    "Year:O",
    title="Year",
    axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
        y=alt.Y(
            "TFR_change_plot:Q",
            title="Annual TFR Change",
            axis=alt.Axis(titleColor="navy", orient="right"), scale=alt.Scale(domain=[-0.14, 0.14])
        ),color=alt.value("navy"),
        tooltip=["Year", "TFR_change"]))

zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="gray").encode(y="y:Q")

prtchanges = (
    alt.layer(gdp_changeprt, tfr_changeprt, zero_line)
    .resolve_scale(y="independent")
    .properties(
        title={"text": "Portugal: Annual GDP Growth and TFR Change",
               "subtitle": "Extreme TFR changes in 1972, 1978, and 1985 clipped to maintain shared scale. Tooltip still indicates correct values."},
        width=700,
        height=320))

st.altair_chart(prtchanges, use_container_width=True)
st.caption("""Portugal exhibits noticeable economic changes alongside a fluctuating pattern of fertility. While economic downturns occasionally coincide with reductions in fertility, the relationship between short-term economic shocks and changes in fertility remains inconsistent. Fertility changes appear gradual and cumulative rather than immediately responsive to individual economic events. This pattern suggests that Portugal’s transition toward very low fertility (seen in previous graphs) may be driven more by long-term structural changes than by short-term economic fluctuations.""")


#USA annual changes graph
usaannydf = merged_all[merged_all["Country"] == "United States"].copy()
usaannydf = usaannydf.sort_values("Year")
usaannydf["TFR_change"] = usaannydf["TFR"].diff()
usaannydf = usaannydf.dropna(subset=["GDP", "TFR_change"]).copy()
usaannydf["Year"] = pd.to_numeric(usaannydf["Year"], errors="coerce")
usaannydf = usaannydf.dropna(subset=["Year"])
usaannydf["Year"] = usaannydf["Year"].astype(int)

gdp_changeusa= (
    alt.Chart(usaannydf)
    .mark_bar(size=10, opacity=0.75)
    .encode(
        x=alt.X("Year:O",title="Year",axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
       y=alt.Y("GDP:Q",title="GDP Growth (%)",
            axis=alt.Axis(titleColor="teal", orient="left"),scale=alt.Scale(domain=[-10, 10]),),
        color=alt.value("teal"),
        tooltip=["Year", "GDP"]))

#for the extreme TFR values
usaannydf["TFR_change_plot"] = usaannydf["TFR_change"].clip(-0.14, 0.14)

tfr_changeusa = (
    alt.Chart(usaannydf)
    .mark_bar(size=3, opacity=0.85)
    .encode(
        x=alt.X(
    "Year:O",
    title="Year",
    axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
        y=alt.Y(
            "TFR_change_plot:Q",
            title="Annual TFR Change",
            axis=alt.Axis(titleColor="navy", orient="right"), scale=alt.Scale(domain=[-0.14, 0.14])
        ),color=alt.value("navy"),
        tooltip=["Year", "TFR_change"]))

zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="gray").encode(y="y:Q")

usachanges = (
    alt.layer(gdp_changeusa, tfr_changeusa, zero_line)
    .resolve_scale(y="independent")
    .properties(
        title={"text": "USA: Annual GDP Growth and TFR Change",
               "subtitle": "Extreme TFR changes in 1962, 1965, 1966, 1967, 1971, and 1972 clipped to maintain shared scale. Tooltip still indicates correct values."},
        width=700,
        height=320))

st.altair_chart(usachanges, use_container_width=True)
st.caption("""In the United States, annual GDP growth fluctuates moderately across decades, while changes in fertility appear comparatively small and irregular after 1973. Fertility changes during the early postwar decades are larger, reflecting the decline following the baby boom period. In many instances, fertility continues its gradual downward trend regardless of temporary economic expansion or contraction, suggesting that longer-term structural factors may play a larger role in shaping fertility patterns than short-term economic conditions. This is underscored by the negative growth in both TFR and GDDP during the Great Recession: the long-term structural decline of the American economy impacted TFR for many years following.""")

#Japan annual changes graph
jpnannydf = merged_all[merged_all["Country"] == "Japan"].copy()
jpnannydf = jpnannydf.sort_values("Year")
jpnannydf["TFR_change"] = jpnannydf["TFR"].diff()
jpnannydf = jpnannydf.dropna(subset=["GDP", "TFR_change"]).copy()
jpnannydf["Year"] = pd.to_numeric(jpnannydf["Year"], errors="coerce")
jpnannydf = jpnannydf.dropna(subset=["Year"])
jpnannydf["Year"] = jpnannydf["Year"].astype(int)

gdp_changejpn= (
    alt.Chart(jpnannydf)
    .mark_bar(size=10, opacity=0.75)
    .encode(
        x=alt.X("Year:O",title="Year",axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
       y=alt.Y("GDP:Q",title="GDP Growth (%)",
            axis=alt.Axis(titleColor="teal", orient="left"),scale=alt.Scale(domain=[-10, 10]),),
        color=alt.value("teal"),
        tooltip=["Year", "GDP"]))

#for the extreme tfr values
jpnannydf["TFR_change_plot"] = jpnannydf["TFR_change"].clip(-0.14, 0.14)

tfr_changejpn = (
    alt.Chart(jpnannydf)
    .mark_bar(size=3, opacity=0.85)
    .encode(
        x=alt.X(
    "Year:O",
    title="Year",
    axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
        y=alt.Y(
            "TFR_change_plot:Q",
            title="Annual TFR Change",
            axis=alt.Axis(titleColor="navy", orient="right"), scale=alt.Scale(domain=[-0.14, 0.14])
        ),color=alt.value("navy"),
        tooltip=["Year", "TFR_change"]))

zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="gray").encode(y="y:Q")

jpnchanges = (
    alt.layer(gdp_changejpn, tfr_changejpn, zero_line)
    .resolve_scale(y="independent")
    .properties(
        title={"text": "Japan: Annual GDP Growth and TFR Change",
               "subtitle": "Extreme TFR changes in 1966, 1967, and 1975 clipped to maintain shared scale. Tooltip still indicates correct values."},
        width=700,
        height=320))

st.altair_chart(jpnchanges, use_container_width=True)
st.caption("""Japan’s chart reveals substantial economic volatility during its rapid postwar growth period, followed by slower but still variable economic performance in later decades. Fertility changes during this period are generally negative, reflecting the country’s sustained fertility decline. While certain economic slowdowns coincide with declines in fertility, the relationship does not appear to be consistently immediate. Instead, fertility in Japan continues its downward trajectory even during periods of economic growth, suggesting that structural demographic and social changes may have a larger impact on fertility rates.""")

#France annual changes graph

fraannydf = merged_all[merged_all["Country"] == "France"].copy()
fraannydf = fraannydf.sort_values("Year")
fraannydf["TFR_change"] = fraannydf["TFR"].diff()
fraannydf = fraannydf.dropna(subset=["GDP", "TFR_change"]).copy()
fraannydf["Year"] = pd.to_numeric(fraannydf["Year"], errors="coerce")
fraannydf = fraannydf.dropna(subset=["Year"])
fraannydf["Year"] = fraannydf["Year"].astype(int)

gdp_changefra= (
    alt.Chart(fraannydf)
    .mark_bar(size=10, opacity=0.75)
    .encode(
        x=alt.X("Year:O",title="Year",axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
       y=alt.Y("GDP:Q",title="GDP Growth (%)",
            axis=alt.Axis(titleColor="teal", orient="left"),scale=alt.Scale(domain=[-10, 10]),),
        color=alt.value("teal"),
        tooltip=["Year", "GDP"]))

tfr_changefra = (
    alt.Chart(fraannydf)
    .mark_bar(size=3, opacity=0.85)
    .encode(
        x=alt.X(
    "Year:O",
    title="Year",
    axis=alt.Axis(
        values=list(range(1960, 2030, 10)),
        labelAngle=0)),
        y=alt.Y(
            "TFR_change:Q",
            title="Annual TFR Change",
            axis=alt.Axis(titleColor="navy", orient="right"), scale=alt.Scale(domain=[-0.14, 0.14])
        ),color=alt.value("navy"),
        tooltip=["Year", "TFR_change"]))

zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="gray").encode(y="y:Q")

frachanges = (
    alt.layer(gdp_changefra, tfr_changefra, zero_line)
    .resolve_scale(y="independent")
    .properties(
        title="France: Annual GDP Growth and TFR Change",
        width=700,
        height=320))

st.altair_chart(frachanges, use_container_width=True)
st.caption("""France shows moderate fluctuations in GDP growth alongside noticeable changes in fertility, particularly during the late 1960s and early 1970s. These larger early declines reflect a structural shift toward lower fertility. After this transition period, annual changes in fertility become smaller and more stable even as GDP growth continues to fluctuate from year to year. While some economic downturns coincide with slight fertility declines, the overall pattern suggests that short-term economic shocks do not consistently produce immediate changes in fertility behavior. Instead, fertility in France appears to evolve through longer-term demographic and social transitions rather than reacting directly to annual economic variation.""")

