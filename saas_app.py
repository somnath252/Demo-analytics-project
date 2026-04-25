import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "Data_file"


def load_csvs():
    accounts = pd.read_csv(DATA_DIR / "ravenstack_accounts.csv", parse_dates=["signup_date"])
    subscriptions = pd.read_csv(DATA_DIR / "ravenstack_subscriptions.csv", parse_dates=["start_date", "end_date"])
    usage = pd.read_csv(DATA_DIR / "ravenstack_feature_usage.csv", parse_dates=["usage_date"])
    tickets = pd.read_csv(
        DATA_DIR / "ravenstack_support_tickets.csv",
        parse_dates=["submitted_at", "closed_at"],
    )
    churn = pd.read_csv(DATA_DIR / "ravenstack_churn_events.csv", parse_dates=["churn_date"])
    return accounts, subscriptions, usage, tickets, churn


def bool_cast(series):
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def clean_accounts(accounts: pd.DataFrame) -> pd.DataFrame:
    accounts = accounts.copy()
    accounts["account_id"] = accounts["account_id"].astype(str)
    accounts["industry"] = accounts["industry"].astype(str).str.strip().str.title()
    accounts["country"] = accounts["country"].astype(str).str.strip().str.upper()
    accounts["plan_tier"] = accounts["plan_tier"].astype(str).str.title()
    accounts["referral_source"] = accounts["referral_source"].astype(str).str.strip().str.lower()
    accounts["seats"] = pd.to_numeric(accounts["seats"], errors="coerce").fillna(0).astype(int)
    accounts["is_trial"] = bool_cast(accounts["is_trial"])
    accounts["churn_flag"] = bool_cast(accounts["churn_flag"])
    accounts["signup_date"] = pd.to_datetime(accounts["signup_date"], errors="coerce")
    return accounts


def clean_subscriptions(subscriptions: pd.DataFrame) -> pd.DataFrame:
    subscriptions = subscriptions.copy()
    subscriptions["subscription_id"] = subscriptions["subscription_id"].astype(str)
    subscriptions["account_id"] = subscriptions["account_id"].astype(str)
    subscriptions["plan_tier"] = subscriptions["plan_tier"].astype(str).str.title()
    subscriptions["billing_frequency"] = subscriptions["billing_frequency"].astype(str).str.lower().replace({"annually": "annual"})
    subscriptions["mrr_amount"] = pd.to_numeric(subscriptions["mrr_amount"], errors="coerce").fillna(0)
    subscriptions["arr_amount"] = pd.to_numeric(subscriptions["arr_amount"], errors="coerce").fillna(0)
    for col in ["is_trial", "upgrade_flag", "downgrade_flag", "churn_flag", "auto_renew_flag"]:
        subscriptions[col] = bool_cast(subscriptions[col])
    subscriptions["start_date"] = pd.to_datetime(subscriptions["start_date"], errors="coerce")
    subscriptions["end_date"] = pd.to_datetime(subscriptions["end_date"], errors="coerce")
    return subscriptions


def clean_usage(usage: pd.DataFrame) -> pd.DataFrame:
    usage = usage.copy()
    usage["subscription_id"] = usage["subscription_id"].astype(str)
    usage["feature_name"] = usage["feature_name"].astype(str).str.strip().str.lower()
    usage["usage_count"] = pd.to_numeric(usage["usage_count"], errors="coerce").fillna(0).astype(int)
    usage["usage_duration_secs"] = pd.to_numeric(usage["usage_duration_secs"], errors="coerce").fillna(0)
    usage["error_count"] = pd.to_numeric(usage["error_count"], errors="coerce").fillna(0).astype(int)
    usage["is_beta_feature"] = bool_cast(usage["is_beta_feature"])
    usage["usage_date"] = pd.to_datetime(usage["usage_date"], errors="coerce")
    usage["session_length_secs"] = np.where(
        usage["usage_count"] > 0,
        usage["usage_duration_secs"] / usage["usage_count"],
        0,
    )
    usage["friction_score"] = np.where(
        usage["usage_count"] > 0,
        usage["error_count"] / usage["usage_count"],
        0,
    )
    return usage


def clean_tickets(tickets: pd.DataFrame) -> pd.DataFrame:
    tickets = tickets.copy()
    tickets["account_id"] = tickets["account_id"].astype(str)
    tickets["priority"] = tickets["priority"].astype(str).str.strip().str.title()
    tickets["satisfaction_score"] = pd.to_numeric(tickets["satisfaction_score"], errors="coerce")
    tickets["escalation_flag"] = bool_cast(tickets["escalation_flag"])
    tickets["submitted_at"] = pd.to_datetime(tickets["submitted_at"], errors="coerce")
    tickets["closed_at"] = pd.to_datetime(tickets["closed_at"], errors="coerce")
    tickets["ticket_latency_hours"] = (tickets["closed_at"] - tickets["submitted_at"]).dt.total_seconds() / 3600
    return tickets


def clean_churn(churn: pd.DataFrame) -> pd.DataFrame:
    churn = churn.copy()
    churn["account_id"] = churn["account_id"].astype(str)
    churn["reason_code"] = churn["reason_code"].astype(str).str.strip().str.lower()
    churn["refund_amount_usd"] = pd.to_numeric(churn["refund_amount_usd"], errors="coerce").fillna(0)
    churn["preceding_upgrade_flag"] = bool_cast(churn["preceding_upgrade_flag"])
    churn["preceding_downgrade_flag"] = bool_cast(churn["preceding_downgrade_flag"])
    churn["is_reactivation"] = bool_cast(churn["is_reactivation"])
    churn["feedback_text"] = churn["feedback_text"].astype(str).replace({"nan": ""})
    churn["churn_date"] = pd.to_datetime(churn["churn_date"], errors="coerce")
    return churn


def build_merged_views(accounts, subscriptions, usage, tickets, churn):
    df_revenue = subscriptions.merge(
        accounts[["account_id", "industry", "country"]], on="account_id", how="left"
    )
    df_usage_value = usage.merge(
        subscriptions[["subscription_id", "mrr_amount", "plan_tier", "account_id"]], on="subscription_id", how="left"
    )
    df_tickets = tickets.merge(
        accounts[["account_id", "industry", "country"]], on="account_id", how="left"
    )
    df_churn = churn.merge(
        accounts[["account_id", "industry", "country"]], on="account_id", how="left"
    )
    return df_revenue, df_usage_value, df_tickets, df_churn


def build_kpis(subscriptions, accounts, churn, tickets):
    total_mrr = subscriptions["mrr_amount"].sum()
    active_subscriptions = subscriptions.loc[subscriptions["churn_flag"] == False].shape[0]
    churn_rate = (churn.shape[0] / max(accounts.shape[0], 1)) * 100
    avg_sat = tickets["satisfaction_score"].mean()
    return total_mrr, active_subscriptions, churn_rate, avg_sat


def render_dashboard():
    st.set_page_config(page_title="RavenStack Executive HQ", layout="wide")
    st.title("🦅 RavenStack Strategic Oversight")
    st.markdown("Internal Analytics: Pilot Phase Data")

    accounts, subscriptions, usage, tickets, churn = load_csvs()
    accounts = clean_accounts(accounts)
    subscriptions = clean_subscriptions(subscriptions)
    usage = clean_usage(usage)
    tickets = clean_tickets(tickets)
    churn = clean_churn(churn)

    df_revenue, df_usage_value, df_tickets, df_churn = build_merged_views(
        accounts, subscriptions, usage, tickets, churn
    )

    total_mrr, active_subscriptions, churn_rate, avg_sat = build_kpis(
        subscriptions, accounts, churn, tickets
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total MRR", f"${total_mrr:,.0f}")
    col2.metric("Active Subscriptions", f"{active_subscriptions:,}")
    col3.metric("Churn Rate", f"{churn_rate:.1f}%")
    col4.metric("Avg Sat Score", f"{avg_sat:.1f}/5")

    st.divider()

    with st.sidebar:
        st.header("Filters")
        industry_filter = st.multiselect(
            "Industry",
            options=sorted(df_revenue["industry"].dropna().unique()),
            default=sorted(df_revenue["industry"].dropna().unique()),
        )
        plan_filter = st.multiselect(
            "Plan tier",
            options=sorted(df_revenue["plan_tier"].dropna().unique()),
            default=sorted(df_revenue["plan_tier"].dropna().unique()),
        )

    filtered_revenue = df_revenue[
        df_revenue["industry"].isin(industry_filter)
        & df_revenue["plan_tier"].isin(plan_filter)
    ]

    tab1, tab2, tab3 = st.tabs(["💰 Revenue & Growth", "📉 Churn Analysis", "🛠️ Product Usage"])

    with tab1:
        st.subheader("Revenue by Industry and Plan")
        fig_rev = px.sunburst(
            filtered_revenue,
            path=["industry", "plan_tier"],
            values="mrr_amount",
            color="mrr_amount",
            color_continuous_scale="RdBu",
        )
        st.plotly_chart(fig_rev, use_container_width=True)

        revenue_by_country = filtered_revenue.groupby("country")["mrr_amount"].sum().reset_index().sort_values(
            "mrr_amount", ascending=False
        )
        fig_country = px.bar(
            revenue_by_country,
            x="country",
            y="mrr_amount",
            title="MRR by Country",
            text="mrr_amount",
        )
        fig_country.update_traces(texttemplate="$%{text:.0f}", textposition="outside")
        st.plotly_chart(fig_country, use_container_width=True)

    with tab2:
        st.subheader("Why are customers leaving?")
        churn_reason = df_churn["reason_code"].fillna("unknown")
        fig_churn = px.pie(
            df_churn,
            names="reason_code",
            hole=0.4,
            title="Churn Reason Distribution",
        )
        st.plotly_chart(fig_churn, use_container_width=True)

        churn_summary = (
            df_churn.groupby("reason_code")["refund_amount_usd"].agg(["count", "sum"]).reset_index()
        )
        churn_summary.columns = ["reason_code", "count", "refund_amount_usd"]
        st.dataframe(churn_summary.sort_values("count", ascending=False), use_container_width=True)

        st.info(
            "💡 Pro Tip: Customers often cite 'pricing', but root causes may show in feature usage friction and support ticket latency."
        )

    with tab3:
        st.subheader("Feature Adoption vs. Error Rates")
        feat_stats = df_usage_value.groupby('feature_name', as_index=False)[['usage_count', 'error_count']].sum()
        fig_scatter = px.scatter(
            feat_stats,
            x="usage_count",
            y="error_count",
            text="feature_name",
            size="error_count",
            color="error_count",
            title="Feature usage vs errors",
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.subheader("Ticket latency by priority")
        ticket_latency = df_tickets.groupby("priority")["ticket_latency_hours"].median().reset_index()
        fig_latency = px.bar(
            ticket_latency,
            x="priority",
            y="ticket_latency_hours",
            title="Median Ticket Latency by Priority",
            text="ticket_latency_hours",
        )
        fig_latency.update_traces(texttemplate="%{text:.1f}h", textposition="outside")
        st.plotly_chart(fig_latency, use_container_width=True)


if __name__ == "__main__":
    render_dashboard()
