# BoE Monetary Policy Agent

## Description 
<p>This is a RAG agent that answers monetary policy question relating to Bank of England's Monetary Committee Policy meetings from Janurary 2013 to Sept 2026. The meeting documents are downloaded from their website. </p>

## TechStack
<ul>
<li>AI Framework - LangChain, Sentence Transformers</li>
<li>Encoding Model - bge-small-en-v1.5</li>
<li>Retrieval - Qdrant</li>
</ul>

## Reports Breakdown
**Total Number Of Reports** - 117 reports. \
**Reports Date Range** - 2013-2026. \
**Types Of Reports** - [minutes, summary, apf, mpr]. 

## Current Version - 0.1
<p>The documents and evaluation pipeline only consume documents from May 2022 to Sept 2026, as they are written in the same format. Documents from a different date range will later be included.</p>

## Architecture