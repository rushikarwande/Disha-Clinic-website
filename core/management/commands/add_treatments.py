from django.core.management.base import BaseCommand
from core.models import Treatment

class Command(BaseCommand):
    help = 'Adds all treatments to the database'

    def handle(self, *args, **kwargs):
        treatments = [
            # General Health
            {
                'name': 'Weight Loss',
                'category': 'general',
                'description': 'Natural and sustainable weight loss treatment using homoeopathic remedies.'
            },
            {
                'name': 'Leprosy',
                'category': 'general',
                'description': 'Comprehensive treatment for leprosy using homoeopathic medicines.'
            },
            {
                'name': 'Height Increase',
                'category': 'general',
                'description': 'Natural treatment to support healthy growth and development in children and adolescents.'
            },
            {
                'name': 'Hemorrhoids',
                'category': 'general',
                'description': 'Effective treatment for hemorrhoids and related symptoms.'
            },
            {
                'name': 'Cold & Allergies',
                'category': 'general',
                'description': 'Treatment for cold, allergies, and related respiratory issues.'
            },
            {
                'name': 'Fissure',
                'category': 'general',
                'description': 'Treatment for anal fissures and related discomfort.'
            },
            {
                'name': 'Asthma & Bile',
                'category': 'general',
                'description': 'Comprehensive treatment for asthma and bile-related issues.'
            },
            {
                'name': 'Fistula',
                'category': 'general',
                'description': 'Treatment for fistula and related conditions.'
            },
            {
                'name': 'Kidney Disorders',
                'category': 'general',
                'description': 'Treatment for various kidney-related conditions.'
            },
            {
                'name': 'Pimples',
                'category': 'skin',
                'description': 'Treatment for acne and pimples using homoeopathic remedies.'
            },
            {
                'name': 'Stomach Disorders',
                'category': 'digestive',
                'description': 'Treatment for various stomach and digestive system disorders.'
            },
            {
                'name': 'Facial Spots',
                'category': 'skin',
                'description': 'Treatment for facial spots and pigmentation issues.'
            },
            {
                'name': 'Arthritis & Knee Pain',
                'category': 'musculoskeletal',
                'description': 'Treatment for arthritis, knee pain, and related joint issues.'
            },
            {
                'name': 'Dandruff & Hair Loss',
                'category': 'skin',
                'description': 'Treatment for dandruff and hair loss issues.'
            },
            {
                'name': 'Heel Pain',
                'category': 'musculoskeletal',
                'description': 'Treatment for heel pain and related foot conditions.'
            },
            {
                'name': 'Premature Hair Greying',
                'category': 'skin',
                'description': 'Treatment for premature greying of hair.'
            },
            {
                'name': 'Body Itching',
                'category': 'skin',
                'description': 'Treatment for various types of body itching and skin conditions.'
            },
            {
                'name': 'Child Irritability',
                'category': 'general',
                'description': 'Treatment for irritability and behavioral issues in children.'
            },
            {
                'name': 'Psoriasis',
                'category': 'skin',
                'description': 'Comprehensive treatment for psoriasis and related skin conditions.'
            },
            {
                'name': 'Homoeopathic Henna',
                'category': 'skin',
                'description': 'Natural hair coloring and treatment using homoeopathic henna.'
            },
            {
                'name': 'Skin Disorders',
                'category': 'skin',
                'description': 'Treatment for various skin disorders and conditions.'
            },
            # Women's Health
            {
                'name': 'Prenatal Treatment',
                'category': 'women',
                'description': 'Specialized treatment for pregnant women and prenatal care.'
            },
            {
                'name': 'Vitiligo',
                'category': 'women',
                'description': 'Treatment for vitiligo and skin pigmentation issues.'
            },
            {
                'name': 'Menstrual Pain',
                'category': 'women',
                'description': 'Treatment for abdominal pain during menstruation.'
            },
            {
                'name': 'Irregular Periods',
                'category': 'women',
                'description': 'Treatment for menstrual irregularities and related issues.'
            },
            {
                'name': 'Infertility',
                'category': 'women',
                'description': 'Comprehensive treatment for infertility issues.'
            },
            {
                'name': 'Anemia',
                'category': 'women',
                'description': 'Treatment for anemia and blood deficiency.'
            },
            {
                'name': 'Uterine Tumors',
                'category': 'women',
                'description': 'Treatment for uterine tumors and related conditions.'
            },
            {
                'name': 'Postmenopausal Disorders',
                'category': 'women',
                'description': 'Treatment for various postmenopausal conditions and symptoms.'
            },
        ]

        for treatment_data in treatments:
            treatment, created = Treatment.objects.get_or_create(
                name=treatment_data['name'],
                defaults=treatment_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created treatment: {treatment.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Treatment already exists: {treatment.name}')) 