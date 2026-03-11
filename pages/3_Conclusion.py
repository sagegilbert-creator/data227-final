import streamlit as st

st.title("Conclusion & Citations")
st.markdown("""Across the visualization, we see a consistent pattern that links economic development and fertility outcomes. Taken together, these visualizations suggest a negative association between economic development and a country's fertility rate, with higher economic growth coinciding with declining birth rates. However, this relationship is not perfectly linear and varies drastically by country. Some countries maintain significantly higher fertility rates while still demonstrating high levels of GDP, while others experience higher fertility rates and extremely low GDP per capita. The ongoing variability suggests that while economic development may play a role in shaping demographic behavior, such as determining fertility outcomes, it is not the sole determinant. Cultural norms, family policies, education levels, labor markets, and more are all strongly associated with total fertility rates across countries. 

Our analysis aims to highlight differences between long-term demographic change and short-term economic fluctuations. While GDP growth rates can vary significantly from year to year, fertility rates change more gradually over long periods. Our bar charts comparing annual GDP and changes in fertility per country demonstrate that these short-term economic changes do not immediately produce large fertility declines or increases. 

Despite the insights provided by our analysis, several limitations remain. Fertility rates and outcomes are influenced by a wide range of factors not explored in this dataset, including healthcare access, childcare availability, education levels, cost of living, and housing markets, to name a few. Without incorporating these variables, we cannot explain why fertility rates differ so much across countries or which variables may be contributing to that. 

Another limitation is that our analysis focuses only on a limited number of (mostly developed) countries. This small sample size limits our ability to generalize our findings and associations to a broader global context, especially because our sample was not representative of all regions or of economic and infrastructural developments. Another note is that we lacked a complete dataset for India because we did not have birth data, which restricted our ability to compare the effects of population size across all of our analyses. Finally, the time span of our analysis was from 1961 to 2022. Despite having almost six decades of data to analyze, our dataset is limited in that we cannot examine longer, more historical demographic transitions in GDP and fertility rates, including periods of conflict such as World Wars I and II.

There are multiple ways we can expand our analysis with additional time and resources. Future directions include incorporating more countries and additional demographic and socioeconomic variables to provide a more comprehensive understanding of how these variables are associated with changes in fertility rates. Further analysis could include longer datasets spanning more years, or even regional data within countries, to identify variations within a country. These branches would allow for a deeper understanding of the complex relationship between economic development and demographic behavior.

In conclusion, our findings show that economic development is strongly associated with declining fertility rates across the United States, India, Portugal, Japan, and France. However, this relationship is shaped by a broader set of socioeconomic and demographic factors, and understanding these interactions is essential for interpreting it and predicting future trends.""")

st.title("Citations")
st.subheader("MLA Format")
st.markdown("""“The Curse of the Fire-Horse: How Superstition Impacted Fertility Rates in Japan.” World Bank Blogs, blogs.worldbank.org/en/opendata/curse-fire-horse-how-superstition-impacted-fertility-rates-japan. 

“Economic Growth, Cultural Traditions, and Declining Fertility.” NBER, www.nber.org/digest/202504/economic-growth-cultural-traditions-and-declining-fertility?page=1&perPage=50. 

BER. “The Japanese Economic Miracle.” Berkeley Economic Review, 26 Jan. 2023, econreview.studentorg.berkeley.edu/the-japanese-economic-miracle/. 

“Skyrocketing Inflation and Japan’s Economic Slowdown. The Global Oil Crisis and Jexim’s Efforts.” Skyrocketing Inflation and Japan’s Economic Slowdown. The Global Oil Crisis and JEXIM’s Efforts | JBIC Japan Bank for International Cooperation, www.jbic.go.jp/en/information/today/today_202307/jtd_202307_column1.html. Accessed 10 Mar. 2026. 

Meyer, Jannik. “How the US Birth Rate Has Evolved over the Past Century.” North American Community Hub, 14 Apr. 2025, nchstats.com/us-birth-rate-over-century/.""")

st.subheader("Data Sources")

st.markdown("""

Human Fertility Database, www.humanfertility.org/Home/Index. 

“Fertility Rate, Total (Births per Woman) - India.” World Bank Open Data, data.worldbank.org/indicator/SP.DYN.TFRT.IN?locations=IN. 

“GDP per Capita (Current US$).” World Bank Open Data, data.worldbank.org/indicator/NY.GDP.PCAP.CD.""")
