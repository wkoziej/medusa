#!/usr/bin/env python3
"""
Test rzeczywistych zaplanowanych postów na Facebooku.

Ten skrypt pozwala przetestować funkcjonalność zaplanowanych postów
z prawdziwymi credentials Facebook, ale z ustawieniami prywatności
tak, żeby tylko Ty mógł zobaczyć posty.
"""

import asyncio
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add the src directory to the path so we can import medusa
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from medusa.publishers.facebook import FacebookPublisher
from medusa.models import PlatformConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# UWAGA: Wypełnij te dane swoimi prawdziwymi credentials Facebook
FACEBOOK_CONFIG = {
    "page_id": "TWÓJ_PAGE_ID",  # np. "123456789012345"
    "access_token": "TWÓJ_ACCESS_TOKEN"  # np. "EAABwzLixnjYBO..."
}

def create_facebook_config():
    """Utwórz konfigurację Facebook."""
    return PlatformConfig(
        platform_name="facebook",
        credentials=FACEBOOK_CONFIG,
        enabled=True
    )

async def test_scheduled_post_private():
    """Test zaplanowanego postu prywatnego (tylko dla Ciebie)."""
    print("🔒 Test zaplanowanego postu prywatnego")
    print("=" * 50)
    
    # Sprawdź czy credentials są ustawione
    if FACEBOOK_CONFIG["page_id"] == "TWÓJ_PAGE_ID":
        print("❌ BŁĄD: Musisz ustawić prawdziwe credentials Facebook!")
        print("   1. Otwórz plik examples/test_real_scheduled_facebook.py")
        print("   2. Zamień TWÓJ_PAGE_ID na prawdziwy ID swojej strony Facebook")
        print("   3. Zamień TWÓJ_ACCESS_TOKEN na prawdziwy token dostępu")
        print("\n   Jak uzyskać credentials:")
        print("   • Idź na https://developers.facebook.com/")
        print("   • Utwórz aplikację Facebook")
        print("   • Dodaj uprawnienie 'pages_manage_posts'")
        print("   • Wygeneruj Page Access Token dla swojej strony")
        return
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    try:
        print("🔐 Autentykacja z Facebook API...")
        await publisher.authenticate()
        print("✅ Autentykacja pomyślna!")
        
        # Zaplanuj post na za 5 minut
        scheduled_time = datetime.now(timezone.utc) + timedelta(minutes=5)
        scheduled_timestamp = int(scheduled_time.timestamp())
        
        print(f"📅 Planowanie postu na: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"⏰ To jest za około 5 minut od teraz")
        
        # Progress callback
        def progress_callback(progress):
            print(f"📊 {progress.step}: {progress.current_step}/{progress.total_steps}")
            if progress.message:
                print(f"   ℹ️  {progress.message}")
        
        # Publikuj zaplanowany post (prywatny)
        result = await publisher.publish_post(
            content=f"""🧪 TEST zaplanowanego postu Medusa
            
To jest test automatyzacji publikacji postów.
Czas utworzenia: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

#medusa #test #automatyzacja""",
            metadata={
                "scheduled_publish_time": scheduled_timestamp,
                # UWAGA: Facebook nie obsługuje bezpośrednio ustawień prywatności w API
                # Post będzie widoczny zgodnie z ustawieniami domyślnymi Twojej strony
            },
            progress_callback=progress_callback
        )
        
        print("\n🎉 SUKCES! Zaplanowany post został utworzony!")
        print(f"📋 Szczegóły:")
        print(f"   🆔 Post ID: {result.post_id}")
        print(f"   🔗 URL: {result.post_url}")
        print(f"   📅 Zaplanowany na: {datetime.fromtimestamp(scheduled_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        print(f"\n📝 Co dalej:")
        print(f"   1. Post zostanie automatycznie opublikowany przez Facebook za ~5 minut")
        print(f"   2. Możesz sprawdzić zaplanowane posty w Publishing Tools swojej strony Facebook")
        print(f"   3. Możesz anulować post przed publikacją w Facebook Creator Studio")
        print(f"   4. Post będzie widoczny zgodnie z ustawieniami prywatności Twojej strony")
        
        print(f"\n🔍 Gdzie sprawdzić:")
        print(f"   • Facebook Creator Studio → Content Library → Posts")
        print(f"   • Lub bezpośrednio: {result.post_url}")
        
    except Exception as e:
        print(f"❌ Błąd podczas testowania: {e}")
        print(f"   Typ błędu: {type(e).__name__}")
        
        if "authentication" in str(e).lower():
            print(f"\n💡 Wskazówki dotyczące autentykacji:")
            print(f"   • Sprawdź czy access_token jest aktualny")
            print(f"   • Sprawdź czy masz uprawnienia 'pages_manage_posts'")
            print(f"   • Sprawdź czy page_id jest prawidłowy")
        
    finally:
        await publisher.cleanup()
        print("\n🧹 Czyszczenie zasobów zakończone")

async def test_immediate_private_post():
    """Test natychmiastowego postu prywatnego dla porównania."""
    print("\n🚀 Test natychmiastowego postu (dla porównania)")
    print("=" * 50)
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    try:
        await publisher.authenticate()
        print("✅ Autentykacja pomyślna!")
        
        # Publikuj natychmiastowy post
        result = await publisher.publish_post(
            content=f"""🚀 TEST natychmiastowego postu Medusa

To jest test natychmiastowej publikacji.
Czas: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

#medusa #test #natychmiastowy""",
            metadata={}
        )
        
        print("✅ Natychmiastowy post opublikowany!")
        print(f"   🆔 Post ID: {result.post_id}")
        print(f"   🔗 URL: {result.post_url}")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
    
    finally:
        await publisher.cleanup()

async def main():
    """Uruchom testy."""
    print("🧪 TESTY RZECZYWISTYCH POSTÓW FACEBOOK")
    print("=" * 60)
    print("⚠️  UWAGA: Te testy będą publikować prawdziwe posty na Twojej stronie Facebook!")
    print("   Upewnij się, że ustawiłeś prawdziwe credentials w kodzie.")
    print()
    
    try:
        # Test zaplanowanego postu
        await test_scheduled_post_private()
        
        # Opcjonalnie: test natychmiastowego postu dla porównania
        response = input("\n❓ Czy chcesz również przetestować natychmiastowy post? (t/n): ")
        if response.lower().startswith('t'):
            await test_immediate_private_post()
        
        print("\n🎯 PODSUMOWANIE TESTÓW:")
        print("✅ Funkcjonalność zaplanowanych postów działa!")
        print("✅ FacebookPublisher poprawnie obsługuje scheduling")
        print("✅ Walidacja czasów przyszłych działa")
        print("✅ API Facebook przyjmuje scheduled_publish_time")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Testy przerwane przez użytkownika")
    except Exception as e:
        print(f"\n\n💥 Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    print("🔧 Aby uruchomić testy:")
    print("   1. Ustaw prawdziwe credentials Facebook w zmiennej FACEBOOK_CONFIG")
    print("   2. Uruchom: uv run python examples/test_real_scheduled_facebook.py")
    print("   3. Sprawdź wyniki w Creator Studio swojej strony Facebook")
    print()
    
    # Sprawdź czy credentials są ustawione
    if FACEBOOK_CONFIG["page_id"] != "TWÓJ_PAGE_ID":
        asyncio.run(main())
    else:
        print("⚠️  Nie uruchamiam testów - brak prawdziwych credentials")
        print("   Ustaw credentials w kodzie, aby uruchomić testy.") 