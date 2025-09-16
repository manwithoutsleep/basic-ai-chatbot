#!/usr/bin/env python3
"""
Phase 5: Visualization and Export Components
Advanced data visualization and export features for the spiritual gifts discovery web app

Key Architecture Concepts:
1. Data Visualization Patterns: Transform AI insights into visual formats
2. Export System Design: Multiple format support for user data
3. Component Modularity: Reusable visualization components
4. User Experience Design: Progressive disclosure of complex data
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any
import base64
from io import BytesIO

class SpiritualGiftsVisualizer:
    """
    Advanced visualization system for spiritual gifts discovery data

    Architecture Pattern: Data Visualization Layer
    - Transforms raw AI insights into meaningful visual representations
    - Provides multiple visualization types for different data aspects
    - Maintains visual consistency and user experience standards
    """

    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'light': '#17becf',
            'themes': {
                'teaching': '#2E8B57',
                'leadership': '#4169E1',
                'helping': '#FF6347',
                'creativity': '#9370DB',
                'justice': '#DC143C',
                'people_focus': '#20B2AA'
            }
        }

    def create_conversation_timeline(self, conversation_history: List[Dict]) -> go.Figure:
        """
        Create interactive timeline of conversation progression

        Architecture Concept: Temporal Data Visualization
        """
        if not conversation_history:
            return self._create_empty_figure("No conversation data available")

        # Prepare timeline data
        timeline_data = []
        for i, exchange in enumerate(conversation_history):
            timeline_data.append({
                'Exchange': i + 1,
                'Timestamp': exchange.get('timestamp', ''),
                'Stage': exchange.get('stage', 'unknown'),
                'User_Words': len(exchange.get('user_input', '').split()),
                'Bot_Words': len(exchange.get('bot_response', '').split()),
                'AI_Reasoning': exchange.get('ai_reasoning', 'No reasoning available')
            })

        df = pd.DataFrame(timeline_data)

        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Conversation Activity', 'Conversation Stages'),
            vertical_spacing=0.1,
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )

        # Word count over time
        fig.add_trace(
            go.Scatter(
                x=df['Exchange'],
                y=df['User_Words'],
                name='Your Word Count',
                line=dict(color=self.color_palette['primary'], width=3),
                mode='lines+markers'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['Exchange'],
                y=df['Bot_Words'],
                name='Guide Response Length',
                line=dict(color=self.color_palette['secondary'], width=2),
                mode='lines+markers'
            ),
            row=1, col=1
        )

        # Stage progression
        stage_colors = {
            'introduction': self.color_palette['themes']['people_focus'],
            'skills_assessment': self.color_palette['themes']['teaching'],
            'passion_exploration': self.color_palette['themes']['creativity'],
            'values_clarification': self.color_palette['themes']['justice'],
            'synthesis': self.color_palette['info']
        }

        for stage in df['Stage'].unique():
            stage_data = df[df['Stage'] == stage]
            fig.add_trace(
                go.Scatter(
                    x=stage_data['Exchange'],
                    y=[stage] * len(stage_data),
                    name=stage.replace('_', ' ').title(),
                    mode='markers',
                    marker=dict(
                        color=stage_colors.get(stage, self.color_palette['light']),
                        size=12,
                        symbol='circle'
                    )
                ),
                row=2, col=1
            )

        fig.update_layout(
            title="Conversation Journey Analysis",
            height=600,
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_xaxes(title_text="Exchange Number", row=2, col=1)
        fig.update_yaxes(title_text="Word Count", row=1, col=1)
        fig.update_yaxes(title_text="Conversation Stage", row=2, col=1)

        return fig

    def create_themes_evolution(self, themes_data: Dict) -> go.Figure:
        """
        Visualize how themes evolved throughout conversation

        Architecture Concept: Pattern Evolution Visualization
        """
        if not themes_data:
            return self._create_empty_figure("No themes identified yet")

        # Prepare themes data
        theme_names = list(themes_data.keys())
        theme_strengths = [themes_data[name].strength for name in theme_names]
        evidence_counts = [len(themes_data[name].evidence) for name in theme_names]

        # Create bubble chart
        fig = go.Figure(data=go.Scatter(
            x=theme_strengths,
            y=evidence_counts,
            mode='markers+text',
            marker=dict(
                size=[s * 20 for s in theme_strengths],  # Scale bubble size
                color=[self.color_palette['themes'].get(name, self.color_palette['primary'])
                      for name in theme_names],
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            text=[name.replace('_', ' ').title() for name in theme_names],
            textposition="middle center",
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{text}</b><br>' +
                         'Strength: %{x:.1f}<br>' +
                         'Evidence Count: %{y}<br>' +
                         '<extra></extra>'
        ))

        fig.update_layout(
            title="Spiritual Gifts Themes - Strength vs Evidence",
            xaxis_title="Theme Strength",
            yaxis_title="Evidence Count",
            height=500,
            showlegend=False
        )

        # Add quadrant lines
        if theme_strengths:
            max_strength = max(theme_strengths)
            max_evidence = max(evidence_counts)

            fig.add_hline(y=max_evidence/2, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=max_strength/2, line_dash="dash", line_color="gray", opacity=0.5)

            # Add quadrant labels
            fig.add_annotation(x=max_strength*0.75, y=max_evidence*0.75,
                             text="Strong & Well-Evidenced", showarrow=False, opacity=0.7)
            fig.add_annotation(x=max_strength*0.25, y=max_evidence*0.75,
                             text="Emerging Pattern", showarrow=False, opacity=0.7)

        return fig

    def create_personality_radar(self, personality_profile) -> go.Figure:
        """
        Create radar chart for personality analysis

        Architecture Concept: Multi-dimensional Data Visualization
        """
        if not personality_profile:
            return self._create_empty_figure("Personality profile still developing...")

        markers = personality_profile.markers

        # Normalize all values to 0-1 scale for radar chart
        dimensions = [
            'Communication Volume',
            'Emotional Expression',
            'Enthusiasm Level',
            'Confidence/Certainty',
            'Concrete Thinking',
            'Question Asking'
        ]

        values = [
            min(markers.word_count_avg / 50, 1.0),  # Normalize word count
            min(markers.emotional_language_frequency * 25, 1.0),  # Scale emotional language
            min(markers.enthusiasm_markers * 15, 1.0),  # Scale enthusiasm
            max(0, 1.0 - markers.uncertainty_indicators * 8),  # Invert uncertainty
            markers.concrete_vs_abstract_ratio,  # Already 0-1
            min(markers.question_asking_frequency * 3, 1.0)  # Scale question frequency
        ]

        # Create radar chart
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=dimensions,
            fill='toself',
            name=f'{personality_profile.primary_style.value.title()} Style',
            line_color=self.color_palette['primary'],
            fillcolor=self.color_palette['primary']
        ))

        # Add average/reference line
        avg_values = [0.5] * len(dimensions)
        fig.add_trace(go.Scatterpolar(
            r=avg_values,
            theta=dimensions,
            fill='none',
            name='Average Profile',
            line=dict(color='gray', dash='dash'),
            opacity=0.5
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickmode='array',
                    tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
                    ticktext=['Low', 'Below Avg', 'Average', 'Above Avg', 'High']
                )
            ),
            showlegend=True,
            title=f"Communication Style Analysis: {personality_profile.primary_style.value.title()}",
            height=500
        )

        return fig

    def create_insights_confidence_chart(self, insights: List) -> go.Figure:
        """
        Visualize AI insights by confidence and type

        Architecture Concept: Confidence Visualization for AI Systems
        """
        if not insights:
            return self._create_empty_figure("No insights discovered yet")

        # Prepare insights data
        insights_data = []
        for insight in insights:
            insights_data.append({
                'Type': insight.insight_type.replace('_', ' ').title(),
                'Confidence': insight.confidence,
                'Stage': insight.stage,
                'Content_Length': len(insight.content),
                'Content_Preview': insight.content[:50] + "..." if len(insight.content) > 50 else insight.content
            })

        df = pd.DataFrame(insights_data)

        # Create scatter plot
        fig = px.scatter(
            df,
            x='Type',
            y='Confidence',
            size='Content_Length',
            color='Stage',
            hover_data=['Content_Preview'],
            title="AI Insights Analysis - Confidence by Type",
            height=500
        )

        # Add confidence threshold line
        fig.add_hline(y=0.8, line_dash="dash", line_color="green",
                     annotation_text="High Confidence Threshold")
        fig.add_hline(y=0.6, line_dash="dash", line_color="orange",
                     annotation_text="Medium Confidence Threshold")

        fig.update_layout(
            xaxis_title="Insight Type",
            yaxis_title="AI Confidence Score",
            showlegend=True
        )

        return fig

    def create_spiritual_gifts_assessment_viz(self, assessment_data: Dict) -> go.Figure:
        """
        Comprehensive spiritual gifts assessment visualization

        Architecture Concept: Multi-metric Dashboard Visualization
        """
        if not assessment_data or 'top_gifts' not in assessment_data:
            return self._create_empty_figure("Complete the discovery journey to see your spiritual gifts assessment")

        # Prepare data
        gifts_data = []
        for gift in assessment_data['top_gifts']:
            gifts_data.append({
                'Gift': gift['name'].title(),
                'Score': gift['score'],
                'Strength': gift['strength'],
                'Description': gift.get('description', '')
            })

        df = pd.DataFrame(gifts_data)

        # Create horizontal bar chart with color coding
        colors = []
        for strength in df['Strength']:
            if strength == 'Dominant':
                colors.append(self.color_palette['success'])
            elif strength == 'Strong':
                colors.append(self.color_palette['primary'])
            elif strength == 'Moderate':
                colors.append(self.color_palette['warning'])
            else:
                colors.append(self.color_palette['light'])

        fig = go.Figure(data=[
            go.Bar(
                y=df['Gift'],
                x=df['Score'],
                orientation='h',
                marker_color=colors,
                text=[f"{score:.1f}% ({strength})" for score, strength in zip(df['Score'], df['Strength'])],
                textposition='inside',
                textfont=dict(color='white', size=12),
                hovertemplate='<b>%{y}</b><br>' +
                             'Score: %{x:.1f}%<br>' +
                             'Strength: %{customdata}<br>' +
                             '<extra></extra>',
                customdata=df['Strength']
            )
        ])

        fig.update_layout(
            title="Your Spiritual Gifts Assessment Results",
            xaxis_title="Gift Strength Score (%)",
            yaxis_title="Spiritual Gifts",
            height=400,
            showlegend=False
        )

        # Add score threshold lines
        fig.add_vline(x=70, line_dash="dash", line_color="green", opacity=0.5)
        fig.add_vline(x=50, line_dash="dash", line_color="orange", opacity=0.5)
        fig.add_vline(x=30, line_dash="dash", line_color="red", opacity=0.5)

        return fig

    def _create_empty_figure(self, message: str) -> go.Figure:
        """Create empty figure with helpful message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=300
        )
        return fig


class ConversationExporter:
    """
    Advanced export system for conversation data

    Architecture Pattern: Multi-format Data Export
    - Supports multiple export formats (JSON, PDF, HTML)
    - Maintains data integrity across formats
    - Provides user-friendly export options
    """

    def __init__(self):
        self.export_formats = ['json', 'html', 'csv']

    def export_conversation_summary(self, session_data: Dict, format_type: str = 'json') -> bytes:
        """
        Export conversation summary in specified format

        Architecture Concept: Format-agnostic Data Export
        """
        if format_type == 'json':
            return self._export_as_json(session_data)
        elif format_type == 'html':
            return self._export_as_html(session_data)
        elif format_type == 'csv':
            return self._export_as_csv(session_data)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def _export_as_json(self, session_data: Dict) -> bytes:
        """Export as structured JSON"""
        export_data = {
            'export_info': {
                'export_date': datetime.now().isoformat(),
                'format': 'json',
                'version': '1.0'
            },
            'session_summary': {
                'total_exchanges': len(session_data.get('conversation_history', [])),
                'session_duration': 'Calculated during export',
                'discovery_stage': session_data.get('current_stage', 'unknown')
            },
            'conversation_data': session_data
        }

        json_string = json.dumps(export_data, indent=2, default=str)
        return json_string.encode('utf-8')

    def _export_as_html(self, session_data: Dict) -> bytes:
        """Export as formatted HTML report"""
        html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Spiritual Gifts Discovery Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f8ff; padding: 20px; border-radius: 10px; }}
        .conversation {{ margin: 20px 0; }}
        .exchange {{ margin: 15px 0; padding: 10px; border-left: 3px solid #ddd; }}
        .user {{ border-left-color: #007bff; background-color: #f8f9fa; }}
        .bot {{ border-left-color: #28a745; background-color: #f1f8e9; }}
        .insights {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Spiritual Gifts Discovery Report</h1>
        <p><strong>Export Date:</strong> {export_date}</p>
        <p><strong>Total Exchanges:</strong> {total_exchanges}</p>
        <p><strong>Discovery Stage:</strong> {stage}</p>
    </div>

    <div class="conversation">
        <h2>Conversation History</h2>
        {conversation_html}
    </div>

    <div class="insights">
        <h2>AI Insights Summary</h2>
        {insights_html}
    </div>
</body>
</html>"""

        # Build conversation HTML
        conversation_html = ""
        for exchange in session_data.get('conversation_history', []):
            conversation_html += f'''
            <div class="exchange user">
                <strong>You:</strong> {exchange.get('user_input', '')}
                <div class="timestamp">{exchange.get('timestamp', '')}</div>
            </div>
            <div class="exchange bot">
                <strong>Guide:</strong> {exchange.get('bot_response', '')}
                {f'<br><em>AI Reasoning: {exchange.get("ai_reasoning", "")}</em>' if exchange.get('ai_reasoning') else ''}
            </div>
            '''

        # Build insights HTML
        insights_html = "<p>Insights analysis would be included here based on session data.</p>"

        # Fill template
        html_content = html_template.format(
            export_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_exchanges=len(session_data.get('conversation_history', [])),
            stage=session_data.get('current_stage', 'unknown').replace('_', ' ').title(),
            conversation_html=conversation_html,
            insights_html=insights_html
        )

        return html_content.encode('utf-8')

    def _export_as_csv(self, session_data: Dict) -> bytes:
        """Export conversation as CSV"""
        # Create DataFrame from conversation history
        conversation_data = []
        for i, exchange in enumerate(session_data.get('conversation_history', [])):
            conversation_data.append({
                'Exchange_Number': i + 1,
                'Timestamp': exchange.get('timestamp', ''),
                'Stage': exchange.get('stage', ''),
                'User_Input': exchange.get('user_input', ''),
                'Bot_Response': exchange.get('bot_response', ''),
                'AI_Reasoning': exchange.get('ai_reasoning', ''),
                'User_Word_Count': len(exchange.get('user_input', '').split()),
                'Bot_Word_Count': len(exchange.get('bot_response', '').split())
            })

        df = pd.DataFrame(conversation_data)

        # Convert to CSV
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        return csv_buffer.getvalue()

    def create_download_link(self, data: bytes, filename: str, format_type: str) -> str:
        """Create download link for exported data"""
        b64_data = base64.b64encode(data).decode()

        mime_types = {
            'json': 'application/json',
            'html': 'text/html',
            'csv': 'text/csv'
        }

        mime_type = mime_types.get(format_type, 'application/octet-stream')

        return f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}">Download {filename}</a>'


# Streamlit components for easy integration
def render_visualization_dashboard(session_state):
    """Render complete visualization dashboard"""
    st.header("📊 Discovery Analytics Dashboard")

    visualizer = SpiritualGiftsVisualizer()

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Timeline", "Themes", "Personality", "Insights"])

    with tab1:
        st.subheader("Conversation Timeline")
        timeline_fig = visualizer.create_conversation_timeline(session_state.conversation_history)
        st.plotly_chart(timeline_fig, use_container_width=True)

    with tab2:
        st.subheader("Themes Evolution")
        if hasattr(session_state, 'context_manager'):
            themes_fig = visualizer.create_themes_evolution(session_state.context_manager.themes)
            st.plotly_chart(themes_fig, use_container_width=True)

    with tab3:
        st.subheader("Personality Analysis")
        if hasattr(session_state, 'personality_profiler'):
            personality_fig = visualizer.create_personality_radar(session_state.personality_profiler.current_profile)
            st.plotly_chart(personality_fig, use_container_width=True)

    with tab4:
        st.subheader("AI Insights Confidence")
        if hasattr(session_state, 'context_manager'):
            insights_fig = visualizer.create_insights_confidence_chart(session_state.context_manager.insights)
            st.plotly_chart(insights_fig, use_container_width=True)

def render_export_options(session_state):
    """Render export options interface"""
    st.header("💾 Export Your Discovery Journey")

    exporter = ConversationExporter()

    col1, col2, col3 = st.columns(3)

    # Prepare session data for export
    session_data = {
        'conversation_history': getattr(session_state, 'conversation_history', []),
        'current_stage': getattr(session_state, 'current_stage', 'unknown'),
        'total_exchanges': getattr(session_state, 'total_exchanges', 0)
    }

    with col1:
        st.subheader("📄 JSON Export")
        st.write("Complete structured data export")
        if st.button("Export as JSON"):
            json_data = exporter.export_conversation_summary(session_data, 'json')
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"spiritual_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    with col2:
        st.subheader("📝 HTML Report")
        st.write("Formatted report for sharing")
        if st.button("Export as HTML"):
            html_data = exporter.export_conversation_summary(session_data, 'html')
            st.download_button(
                label="📥 Download HTML",
                data=html_data,
                file_name=f"spiritual_discovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html"
            )

    with col3:
        st.subheader("📊 CSV Data")
        st.write("Spreadsheet-compatible format")
        if st.button("Export as CSV"):
            csv_data = exporter.export_conversation_summary(session_data, 'csv')
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"spiritual_discovery_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )