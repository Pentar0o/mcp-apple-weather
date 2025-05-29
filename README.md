# Serveur MCP Apple Weather

Un serveur Model Context Protocol (MCP) qui intègre l'API Apple WeatherKit pour fournir des prévisions météo directement dans Claude Desktop.

## Vue d'ensemble

Ce serveur MCP permet à Claude de récupérer des données météo en temps réel en utilisant le service WeatherKit d'Apple. Il fournit des prévisions météo précises et des résumés pour n'importe quelle ville dans le monde, intégrés de manière transparente dans vos conversations Claude Desktop.

## Fonctionnalités

- 🌤️ **Prévisions météo détaillées** : Obtenez des prévisions quotidiennes complètes incluant température, précipitations, vitesse du vent et conditions météo
- 📊 **Résumés météo** : Aperçu rapide de la météo pour aujourd'hui et demain
- 🌍 **Support international** : Fonctionne avec des villes du monde entier en utilisant les codes pays
- 🔄 **Données en temps réel** : Intégration directe avec Apple WeatherKit pour des informations précises et à jour

## Prérequis

Avant l'installation, assurez-vous d'avoir :

1. **Claude Desktop** installé sur votre système
2. **Un compte Apple Developer** avec le service WeatherKit activé
3. **Les certificats WeatherKit** : 
   - Clé privée (fichier .p8)
   - Key ID et Team ID depuis le portail Apple Developer
4. **Python 3.8+** installé sur votre système

## Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/Pentar0o/mcp-apple-weather.git
cd mcp-apple-weather
```

2. Installez les dépendances :
```bash
pip3 install -r requirements.txt --break-system-packages
```

3. Configurez vos identifiants Apple :
   - Copiez `.env.example` vers `.env`
   - Remplissez vos identifiants dans `.env`
   - Placez vos certificats `.p8` dans le dossier `certificats/`

4. Rendez le script de lancement exécutable :
```bash
chmod +x run_server.sh
```

## Configuration

### Configuration des identifiants

1. Créez un fichier `.env` à partir de `.env.example` :
```bash
cp .env.example .env
```

2. Éditez `.env` avec vos identifiants Apple :
```
WEATHER_KEY_ID=YOUR_WEATHER_KEY_ID
MAP_KEY_ID=YOUR_MAP_KEY_ID
TEAM_ID=YOUR_TEAM_ID
SERVICE_ID=com.example.weatherapp
```

3. Placez vos certificats dans le dossier `certificats/` :
   - `certificats/AuthKey_Weather.p8`
   - `certificats/AuthKey_Mapkit.p8`

### Configuration de Claude Desktop

Ajoutez le serveur à votre fichier de configuration Claude Desktop :

**Sur macOS :** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Sur Linux :** `~/.config/claude/claude_desktop_config.json`  
**Sur Windows :** `%APPDATA%\claude\claude_desktop_config.json`

#### Méthode recommandée (avec script wrapper) :

```json
{
  "mcpServers": {
    "apple-weather": {
      "command": "/chemin/vers/votre/mcp-apple-weather/run_server.sh"
    }
  }
}
```

#### Méthode alternative (directe) :

```json
{
  "mcpServers": {
    "apple-weather": {
      "command": "python3",
      "args": ["server.py"],
      "cwd": "/chemin/vers/votre/mcp-apple-weather"
    }
  }
}
```

**Note importante** : Utilisez `mcpServers` et non `servers` dans la configuration.

### Redémarrage de Claude Desktop

Après avoir modifié la configuration :
1. Quittez complètement Claude Desktop (⌘+Q sur macOS)
2. Relancez Claude Desktop
3. L'intégration devrait apparaître dans les outils disponibles

## Utilisation

Une fois configuré, vous pouvez utiliser ces commandes dans Claude Desktop :

### Obtenir les prévisions météo
Demandez à Claude : "Quelle est la météo à Paris ?" ou "Donne-moi les prévisions pour Tokyo, Japon"

### Obtenir un résumé météo
Demandez à Claude : "Donne-moi un résumé rapide de la météo à Londres"

## Structure du projet

```
mcp-apple-weather/
├── server.py           # Serveur MCP principal
├── weather.py          # Intégration WeatherKit
├── maps.py            # Géocodage avec Apple Maps
├── auth.py            # Authentification JWT
├── utils.py           # Fonctions utilitaires
├── app_config.py      # Configuration
├── run_server.sh      # Script de lancement
├── certificats/       # Dossier pour les certificats .p8
├── logs/              # Logs du serveur
└── cache/             # Cache (futur)
```

## Dépannage

### Problèmes courants

1. **L'intégration n'apparaît pas dans Claude Desktop**
   - Vérifiez que vous utilisez `mcpServers` et non `servers` dans la configuration
   - Assurez-vous que le chemin vers le script est correct et absolu
   - Redémarrez complètement Claude Desktop

2. **"Certificats Apple WeatherKit manquants"**
   - Vérifiez que vos certificats .p8 sont dans le dossier `certificats/`
   - Vérifiez les noms de fichiers dans `app_config.py`

3. **"Failed to import weather module"**
   - Vérifiez que tous les fichiers Python sont présents
   - Installez les dépendances : `pip3 install -r requirements.txt --break-system-packages`

4. **Aucune donnée météo retournée**
   - Vérifiez vos identifiants Apple dans `.env`
   - Vérifiez que WeatherKit est activé sur votre compte Developer

### Vérifier les logs

Pour déboguer, consultez les logs de Claude Desktop :
- **macOS** : `~/Library/Logs/Claude/`
- Ou utilisez Console.app et recherchez "Claude"

## Licence

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails

## Auteur

Créé par Pentar0o

---

Créé avec ❤️ pour la communauté Claude Desktop
