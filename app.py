    
    # Create visualizations
    plots = []

    # Session Time Over Time
    fig1 = px.line(df, x='Created At', y='Time', title='Session Time Over Time')
    fig1.update_layout(xaxis_title='Date', yaxis_title='Session Time (minutes)', xaxis=dict(tickangle=45))
    plots.append(fig1.to_html(full_html=False))

    # Goal Distribution
    fig2 = px.histogram(df, x='Goal', title='Goal Distribution')
    fig2.update_layout(xaxis_title='Goal', yaxis_title='Count', xaxis=dict(tickangle=45))
    plots.append(fig2.to_html(full_html=False))

    # Session Duration Distribution
    fig3 = px.histogram(df, x='Time', nbins=20, title='Session Duration Distribution')
    fig3.update_layout(xaxis_title='Session Duration (minutes)', yaxis_title='Frequency')
    plots.append(fig3.to_html(full_html=False))

    # Total Elapsed Time by Goal (Excluding 60-min Sessions)
    fig4 = px.bar(df_filtered, x='Goal', y='Elapsed', title='Total Elapsed Time by Goal (Excluding 60-min Sessions)', 
                  labels={'Elapsed':'Total Elapsed Time (minutes)'})
    fig4.update_layout(xaxis=dict(tickangle=45))
    plots.append(fig4.to_html(full_html=False))

    # Session Time vs Elapsed Time (Excluding 60-min Sessions)
    fig5 = px.scatter(df_filtered, x='Time', y='Elapsed', title='Session Time vs Elapsed Time (Excluding 60-min Sessions)')
    fig5.update_layout(xaxis_title='Session Time (minutes)', yaxis_title='Elapsed Time (minutes)')
    plots.append(fig5.to_html(full_html=False))

    return render_template('index.html', plots=plots)