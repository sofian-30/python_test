import time
import pandas as pd

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

def get_filters():
    """
    Demande à l'utilisateur de spécifier une ville, un mois et un jour à analyser.

    Retourne:
        (str) ville - nom de la ville à analyser
        (str) mois - nom du mois à filtrer, ou "all" pour appliquer aucun filtre de mois
        (str) jour - nom du jour de la semaine à filtrer, ou "all" pour appliquer aucun filtre de jour
    """
    print("Bonjour! Explorons les données des vélos en libre-service!")

    villes = ["chicago", "new york city", "washington"]
    mois_options = ["all", "january", "february", "march", "april", "may", "june"]
    jours_options = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    while True:
        ville = input("Veuillez choisir une ville (chicago, new york city, washington): ").lower()
        if ville in villes:
            break
        else:
            print("Entrée invalide. Veuillez réessayer.")

    while True:
        mois = input("Veuillez choisir un mois (all, january, february, ... , june): ").lower()
        if mois in mois_options:
            break
        else:
            print("Entrée invalide. Veuillez réessayer.")

    while True:
        jour = input("Veuillez choisir un jour de la semaine (all, monday, tuesday, ... sunday): ").lower()
        if jour in jours_options:
            break
        else:
            print("Entrée invalide. Veuillez réessayer.")

    print("-" * 40)
    return ville, mois, jour

def load_data(ville, mois, jour):
    """
    Charge les données pour la ville spécifiée et filtre par mois et jour si applicable.

    Args:
        (str) ville - nom de la ville à analyser
        (str) mois - nom du mois à filtrer, ou "all" pour appliquer aucun filtre de mois
        (str) jour - nom du jour de la semaine à filtrer, ou "all" pour appliquer aucun filtre de jour
    Retourne:
        df - DataFrame Pandas contenant les données de la ville filtrées par mois et jour
    """
    # Utiliser l'encodage latin1 pour lire le fichier CSV
    df = pd.read_csv(CITY_DATA[ville], encoding='latin1')

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if mois != 'all':
        mois_index = ["january", "february", "march", "april", "may", "june"].index(mois) + 1
        df = df[df['month'] == mois_index]

    if jour != 'all':
        df = df[df['day_of_week'] == jour.title()]

    return df

def time_stats(df):
    """Affiche des statistiques sur les moments les plus fréquents de déplacement."""

    print("\nCalcul des moments les plus fréquents de déplacement...\n")
    start_time = time.time()

    # Afficher le mois le plus commun
    common_month = df['month'].mode()[0]
    print(f"Mois le plus commun : {common_month}")

    # Afficher le jour de la semaine le plus commun
    common_day_of_week = df['day_of_week'].mode()[0]
    print(f"Jour de la semaine le plus commun : {common_day_of_week}")

    # Afficher l'heure de début la plus commune
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print(f"Heure de début la plus commune : {common_start_hour}")

    print("\nCela a pris %s secondes." % (time.time() - start_time))
    print("-" * 40)

def station_stats(df):
    """Affiche des statistiques sur les stations et trajets les plus populaires."""

    print("\nCalcul des stations et trajets les plus populaires...\n")
    start_time = time.time()

    # Afficher la station de départ la plus utilisée
    common_start_station = df['Start Station'].mode()[0]
    print(f"Station de départ la plus utilisée : {common_start_station}")

    # Afficher la station d'arrivée la plus utilisée
    common_end_station = df['End Station'].mode()[0]
    print(f"Station d'arrivée la plus utilisée : {common_end_station}")

    # Afficher la combinaison de départ et d'arrivée la plus fréquente
    df['start_end_combination'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['start_end_combination'].mode()[0]
    print(f"Combinaison de départ et d'arrivée la plus fréquente : {common_trip}")

    print("\nCela a pris %s secondes." % (time.time() - start_time))
    print("-" * 40)

def trip_duration_stats(df):
    """Affiche des statistiques sur la durée totale et moyenne des trajets."""

    print("\nCalcul de la durée des trajets...\n")
    start_time = time.time()

    # Afficher la durée totale des trajets
    total_travel_time = df['Trip Duration'].sum()
    print(f"Durée totale des trajets : {total_travel_time} secondes")

    # Afficher la durée moyenne des trajets
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Durée moyenne des trajets : {mean_travel_time} secondes")

    print("\nCela a pris %s secondes." % (time.time() - start_time))
    print("-" * 40)

def user_stats(df):
    """Affiche des statistiques sur les utilisateurs de vélos en libre-service."""

    print("\nCalcul des statistiques sur les utilisateurs...\n")
    start_time = time.time()

    # Afficher le nombre de chaque type d'utilisateur
    user_types = df['User Type'].value_counts()
    print(f"Nombre de chaque type d'utilisateur :\n{user_types}")

    # Afficher le nombre de chaque genre
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"\nNombre de chaque genre :\n{gender_counts}")

    # Afficher l'année de naissance la plus ancienne, la plus récente et la plus commune
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print(f"\nAnnée de naissance la plus ancienne : {earliest_year}")
        print(f"Année de naissance la plus récente : {most_recent_year}")
        print(f"Année de naissance la plus commune : {most_common_year}")

    print("\nCela a pris %s secondes." % (time.time() - start_time))
    print("-" * 40)

def main():
    while True:
        ville, mois, jour = get_filters()
        df = load_data(ville, mois, jour)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nVoulez-vous recommencer? Entrez 'oui' ou 'non'.\n")
        if restart.lower() != "oui":
            break

if __name__ == "__main__":
    main()
