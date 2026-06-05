make create-migration MIGRATION_NAME=create_i18n_coll

src/
└── core/
    ├── domain/            # Suas entidades de negócio
    ├── usecases/          # Seus casos de uso (orquestração)
    │
    # Recursos transversais compartilhados pelo sistema:
    ├── logging/           # Gerenciamento de logs e rastreabilidade
    │   └── logger.py
    ├── security/          # Criptografia, hashing de senhas, JWT
    │   └── crypto.py
    └── exceptions/        # Exceções de negócio globais
        └── business.py




# Why Database Migrations are Essential in Robust Architectures

When building a fast-scaling financial services startup, engineering teams must prioritize speed, predictability, and system resilience. While MongoDB is technically "schemaless" and capable of creating collections and inserting documents on the fly (for example, via an `upsert=True` repository operation), relying on this behavior in production introduces significant architectural debt.

In a robust, production-grade microservice architecture, **migrations are not optional luxuries—they are strict engineering requirements for governance, predictability, and safety.**

---

## Core Pillars of Database Migrations

### 1. Controlled Schema Evolution (Yes, Even in NoSQL)
Saying MongoDB is *schemaless* is a technical myth. The database engine might not enforce a schema, but your application **does** (via domain entities and Pydantic/Beanie models).

* **The Problem:** If Version 1 of a service expects a field `text: str`, and Version 2 evolves to support dynamic markdown with `rich_text: dict`, any old documents left in the database will cause Version 2 of your code to crash upon deserialization.
* **The Migration Solution:** Migrations provide a structured, automated `Forward` path to transform and update legacy documents in bulk *before* the new application code goes live.

### 2. Index Management and Production Performance
For a database to perform efficiently under load, it requires carefully planned indexes (such as a unique constraint on `locale_key`). Leaving MongoDB to provision collections on demand means it will only generate the default `_id` index.

* **The Risk:** Deploying a service that queries millions of documents by an unindexed field causes a *Full Collection Scan*. This leads to CPU spikes, API latency, and in critical scenarios, database downtime.
* **The Migration Solution:** Migrations guarantee that all crucial performance indexes and uniqueness constraints are applied to the database instance well before live production traffic arrives.

### 3. Team Alignment and Deterministic Environments
As the startup grows and multiple engineers begin developing in parallel across different local branches:

* **Without Migrations:** Synchronizing local environments becomes chaotic. Engineers have to manually export/import database dumps or run raw scripts to match the state of another teammate's database.
* **With Migrations:** A developer pulls the latest branch, runs a single command (e.g., `make run-dev` or `beanie upgrade`), and their local database seamlessly equalizes to the exact state of the rest of the team in seconds.

### 4. CI/CD Automation and Isolated Environments
To achieve true continuous deployment, human intervention in database states must be eliminated across `Development`, `Staging`, and `Production` environments.

* Raw database access to manually tweak collections or seed values in production is a major security and stability risk.
* CI/CD pipelines leverage the migration history to automatically prepare, seed, and update isolated environments. If a deployment fails, the pipeline can safely invoke a `Backward` (`downgrade`) migration to revert the database to its last known stable state.

### 5. Idempotence and Reproducibility
The defining characteristic of a well-structured migration (leveraging atomic operators and framework lifecycle checks) is **idempotence**: the ability to execute the exact same script multiple times without causing side effects, state corruption, or data duplication. If a container crashes mid-deployment and restarts, the migration system securely tracks precisely where it left off.

---

## Summary for Startup Vision

Cutting corners by allowing the code to implicitly generate database structures creates the illusion of speed early on, but quickly mutates into operational instability. Implementing a strict migration workflow guarantees the **architectural peace** required to scale the platform safely, predictably, and resiliently.
