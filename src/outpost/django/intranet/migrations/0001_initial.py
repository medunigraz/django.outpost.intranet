# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 08:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    ops = [
        (
            """
            CREATE SCHEMA IF NOT EXISTS "intranet";
            """,
            """
            DROP SCHEMA IF EXISTS "intranet";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "intranet"."blogs" (
                id int4 NULL,
                created timestamptz NULL,
                modified timestamptz NULL,
                xmldata xml NULL
            )
            SERVER sqlalchemy
            OPTIONS (
                SCHEMA 'viewData',
                tablename 'blogs',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("intranet-wss")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "intranet"."blogs";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "intranet"."news" (
                id int4 NULL,
                created timestamptz NULL,
                modified timestamptz NULL,
                xmldata xml NULL
            )
            SERVER sqlalchemy
            OPTIONS (
                SCHEMA 'viewData',
                tablename 'news',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("intranet-wss")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "intranet"."news";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "intranet"."mailings" (
                id int4 NULL,
                title text NULL,
                description text NULL,
                shortdescription text NULL,
                startdate timestamp NULL,
                enddate timestamp NULL,
                keyword varchar NULL,
                distributionmembers text NULL,
                created timestamp NULL,
                published boolean NULL,
                begin timestamp NULL,
                units varchar NULL,
                visiblefor varchar NULL,
                headerimage bytea NULL,
                headerimagename varchar NULL
            )
            SERVER sqlalchemy
            OPTIONS (
                SCHEMA 'dbo',
                tablename 'Mailings',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("intranet-icc")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "intranet"."mailings";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."intranet_blog" AS SELECT
                b.id::integer AS id,
                b.created AS created,
                b.modified AS modified,
                array_to_string(xpath('/blog/datetime1/text()', xmlelement(name blog, b.xmldata)), '')::timestamp AT TIME ZONE '{tz}' AS published,
                array_to_string(xpath('/blog/nvarchar1/text()', xmlelement(name blog, b.xmldata)), '') AS title,
                html_unescape(array_to_string(xpath('/blog/ntext2/text()', xmlelement(name blog, b.xmldata)), '')) AS body,
                array_to_string(xpath('/blog/nvarchar6/text()', xmlelement(name blog, b.xmldata)), '') AS author,
                regexp_split_to_array(array_to_string(xpath('/blog/nvarchar3/text()', xmlelement(name blog, b.xmldata)), ''), '\s*;\s*') AS target,
                array_to_string(xpath('/blog/ntext4/text()', xmlelement(name blog, b.xmldata)), '') AS image
            FROM "intranet"."blogs" b
            WITH DATA;
            """.format(
                tz=settings.TIME_ZONE
            ),
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."intranet_blog";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."intranet_news" AS SELECT
                n.id::integer AS id,
                n.created AS created,
                n.modified AS modified,
                array_to_string(xpath('/news/datetime1/text()', xmlelement(name news, n.xmldata)), '')::timestamp AT TIME ZONE '{tz}' AS published,
                trim(html_unescape(array_to_string(xpath('/news/ntext2/text()', xmlelement(name news, n.xmldata)), ''))) AS title,
                html_unescape(array_to_string(xpath('/news/ntext3/text()', xmlelement(name news, n.xmldata)), '')) AS body,
                array_to_string(xpath('/news/ntext5/text()', xmlelement(name news, n.xmldata)), '') AS image,
                NULLIF(array_to_string(xpath('/news/ntext6/text()', xmlelement(name news, n.xmldata)), ''), '')::jsonb AS "json",
                regexp_split_to_array(array_to_string(xpath('/news/nvarchar5/text()', xmlelement(name news, n.xmldata)), ''), '\s*;\s*') AS target
            FROM "intranet"."news" "n"
            WITH DATA;
            """.format(
                tz=settings.TIME_ZONE
            ),
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."intranet_news";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."intranet_mailing" AS SELECT
                m.id::integer AS id,
                m.created AT TIME ZONE '{tz}' AS created,
                m.startdate AT TIME ZONE '{tz}' AS start,
                m.enddate AT TIME ZONE '{tz}' AS "end",
                m.title AS title,
                m.shortdescription AS short,
                m.description AS body,
                (SELECT array_agg(trim(t.e)) from (SELECT unnest(string_to_array(m.keyword, ';')) e) t) AS keywords,
                (SELECT array_agg(trim(t.e)) from (SELECT unnest(string_to_array(m.distributionmembers, ';')) e) t) AS members,
                (SELECT array_agg(trim(t.e)) from (SELECT unnest(regexp_split_to_array(m.visiblefor, '\s*;\s*')) e) t) AS target,
                m.headerimage AS image
            FROM "intranet"."mailings" "m"
            WHERE
                m.published IS TRUE
            WITH DATA;
            """.format(
                tz=settings.TIME_ZONE
            ),
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."intranet_mailing";
            """,
        ),
    ]

    dependencies = [("base", "0001_initial")]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
