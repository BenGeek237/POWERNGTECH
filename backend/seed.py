import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.formations.models import Category as FormationCategory, Formation, Chapitre, Video
from apps.boutique.models import ProductCategory, Product
from apps.services.models import Service

def clear_db():
    print("Clearing old data...")
    Video.objects.all().delete()
    Chapitre.objects.all().delete()
    Formation.objects.all().delete()
    FormationCategory.objects.all().delete()
    Product.objects.all().delete()
    ProductCategory.objects.all().delete()
    Service.objects.all().delete()

def seed_services():
    print("Seeding services...")
    services = [
        {
            "title": "Installation de panneaux solaires",
            "description": "Nous installons des systèmes photovoltaïques complets pour les particuliers et les entreprises. Réduisez vos factures d'énergie dès aujourd'hui.",
            "icon": "Sun",
            "order": 1
        },
        {
            "title": "Maintenance et Dépannage",
            "description": "Entretien préventif et dépannage de vos installations électriques, solaires et réseaux pour garantir une performance optimale.",
            "icon": "Wrench",
            "order": 2
        },
        {
            "title": "Audit Énergétique",
            "description": "Analyse complète de votre consommation énergétique pour vous proposer les solutions les plus rentables et durables.",
            "icon": "ChartBar",
            "order": 3
        }
    ]
    for s in services:
        Service.objects.create(**s)

def seed_formations():
    print("Seeding formations...")
    # Categories
    cat_solaire = FormationCategory.objects.create(name="Énergie Solaire", slug="energie-solaire", icon="Sun", description="Formations sur les systèmes solaires photovoltaïques")
    cat_elec = FormationCategory.objects.create(name="Électronique", slug="electronique", icon="Bolt", description="Apprenez les bases et l'électronique avancée")

    # Formations
    f1 = Formation.objects.create(
        title="Formation complète en Énergie Solaire",
        slug="formation-complete-energie-solaire",
        category=cat_solaire,
        description="Maîtrisez l'installation, le dimensionnement et la maintenance des panneaux solaires photovoltaïques.",
        objectives="Comprendre le fonctionnement des panneaux solaires\nDimensionner un système autonome\nInstaller et maintenir un système",
        prerequisites="Aucun prérequis technique, être motivé",
        price=50000,
        is_free=False,
        level="DEBUTANT",
        duration_hours=15.5,
        status="PUBLIE",
        is_featured=True
    )

    f2 = Formation.objects.create(
        title="Initiation à l'Électronique Pratique",
        slug="initiation-electronique-pratique",
        category=cat_elec,
        description="Plongez dans le monde de l'électronique. Apprenez à souder, à lire un schéma et à créer vos propres circuits.",
        objectives="Savoir lire un schéma électronique\nUtiliser un multimètre\nRéaliser des circuits simples",
        prerequisites="Savoir lire et écrire",
        price=0,
        is_free=True,
        level="DEBUTANT",
        duration_hours=5.0,
        status="PUBLIE",
        is_featured=False
    )

    # Chapters & Videos for f1
    c1 = Chapitre.objects.create(formation=f1, title="Introduction à l'énergie solaire", order=1)
    Video.objects.create(chapter=c1, title="Le rayonnement solaire", duration_minutes=15, order=1, is_preview=True)
    Video.objects.create(chapter=c1, title="Les types de panneaux", duration_minutes=20, order=2)

    c2 = Chapitre.objects.create(formation=f1, title="Dimensionnement", order=2)
    Video.objects.create(chapter=c2, title="Calcul des besoins énergétiques", duration_minutes=35, order=1)

    # Chapters & Videos for f2
    c3 = Chapitre.objects.create(formation=f2, title="Les composants de base", order=1)
    Video.objects.create(chapter=c3, title="Résistances et condensateurs", duration_minutes=12, order=1, is_preview=True)

def seed_boutique():
    print("Seeding boutique...")
    pc_panneaux = ProductCategory.objects.create(name="Panneaux Solaires", slug="panneaux-solaires")
    pc_batteries = ProductCategory.objects.create(name="Batteries", slug="batteries")
    pc_outils = ProductCategory.objects.create(name="Outillage", slug="outillage")

    Product.objects.create(
        name="Panneau Solaire Monocristallin 330W",
        slug="panneau-solaire-mono-330w",
        category=pc_panneaux,
        description="Panneau solaire haute efficacité pour installations résidentielles.",
        price=85000,
        stock=50,
        is_available=True,
        is_featured=True
    )

    Product.objects.create(
        name="Batterie Gel 12V 100Ah",
        slug="batterie-gel-12v-100ah",
        category=pc_batteries,
        description="Batterie à décharge profonde idéale pour les systèmes solaires autonomes.",
        price=120000,
        stock=20,
        is_available=True,
        is_featured=True
    )

    Product.objects.create(
        name="Multimètre Numérique Pro",
        slug="multimetre-numerique-pro",
        category=pc_outils,
        description="Multimètre précis pour toutes vos mesures électriques et électroniques.",
        price=15000,
        stock=100,
        is_available=True,
        is_featured=False
    )

if __name__ == "__main__":
    clear_db()
    seed_services()
    seed_formations()
    seed_boutique()
    print("Database seeded successfully with dummy data!")
