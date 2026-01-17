
from app import app, db
from models import Course, Module, Lesson, Quiz, Question, Option, CourseCategory, CourseLevel
from sqlalchemy import text

def seed_translations():
    print("🌍 Seeding Multilingual Content (FR/EN/AR)...")
    
    # --- HELPER: Upsert Translation ---
    def upsert_trans(table, id_col, id_val, lang, title, desc=None, content=None):
        # Build dynamic query
        cols = ["lang", id_col, "title"]
        vals = [":lang", ":id", ":title"]
        params = {"lang": lang, "id": id_val, "title": title}
        
        if desc is not None:
            cols.append("description")
            vals.append(":desc")
            params["desc"] = desc
        
        if content is not None:
            cols.append("content")
            vals.append(":content")
            params["content"] = content
            
        sql = text(f"""
            INSERT INTO {table} ({', '.join(cols)})
            VALUES ({', '.join(vals)})
            ON DUPLICATE KEY UPDATE 
            title = VALUES(title)
            {', description = VALUES(description)' if desc is not None else ''}
            {', content = VALUES(content)' if content is not None else ''}
        """)
        
        db.session.execute(sql, params)
        db.session.commit()

    # --- 1. COURSE TRANSLATIONS ---
    # Course 1: Institutional Trading
    c1 = Course.query.filter(Course.title.like("%Institutional%")).first()
    if c1:
        print(f"Translating Course: {c1.title}")
        upsert_trans("course_translations", "course_id", c1.id, "fr", 
                     "Maîtrise du Trading Institutionnel", 
                     "Maîtrisez les Order Blocks, la Liquidité et la Structure de Marché comme les pros.")
        upsert_trans("course_translations", "course_id", c1.id, "en", 
                     "Institutional Trading Mastery", 
                     "Master Order Blocks, Liquidity, and Market Structure like the pros.")
        upsert_trans("course_translations", "course_id", c1.id, "ar", 
                     "احتراف التداول المؤسسي", 
                     "أتقن كتل الأوامر، والسيولة، وهيكل السوق مثل المحترفين.")

        # --- MODULES & LESSONS ---
        # M1: Market Structure
        m1 = Module.query.filter_by(course_id=c1.id, order=1).first()
        if m1:
            upsert_trans("module_translations", "module_id", m1.id, "fr", "Fondamentaux de la Structure")
            upsert_trans("module_translations", "module_id", m1.id, "en", "Market Structure Fundamentals")
            upsert_trans("module_translations", "module_id", m1.id, "ar", "أساسيات هيكل السوق")
            
            # Lessons M1
            lessons = Lesson.query.filter_by(module_id=m1.id).all()
            for l in lessons:
                if "Intro" in l.title or "Intro" in l.content: # Approximate match
                    upsert_trans("lesson_translations", "lesson_id", l.id, "fr", 
                                 "Introduction à la Structure de Marché", 
                                 content="## Qu'est-ce que la Structure ?\nLa structure définit la tendance (HH/HL).\n\n### Concepts Clés\n- **Hausse**: Hauts plus hauts\n- **Baisse**: Bas plus bas\n\nTradez toujours AVEC la structure.")
                    upsert_trans("lesson_translations", "lesson_id", l.id, "en", 
                                 "Introduction to Market Structure", 
                                 content="## What is Market Structure?\nIt defines trend direction using swing highs and lows.\n\n### Core Concepts\n- **Uptrend**: Higher Highs (HH)\n- **Downtrend**: Lower Lows (LL)\n\nAlways trade WITH the structure.")
                    upsert_trans("lesson_translations", "lesson_id", l.id, "ar", 
                                 "مقدمة في هيكل السوق", 
                                 content="## ما هو هيكل السوق؟\nيحدد اتجاه الترند باستخدام القمم والقيعان.\n\n### المفاهيم الأساسية\n- **اتجاه صاعد**: قمم أعلى وقيعان أعلى\n- **اتجاه هابط**: قيعان أدنى وقمم أدنى\n\nتداول دائمًا مع الهيكل.")
                
                elif "BOS" in l.title:
                    upsert_trans("lesson_translations", "lesson_id", l.id, "fr",
                                 "Cassure de Structure (BOS)",
                                 content="## BOS Expliqué\nUne cassure confirme la continuation.\n\n### Comment Trader\n1. Attendre la cassure\n2. Attendre le pullback\n3. Entrer sur confirmation")
                    upsert_trans("lesson_translations", "lesson_id", l.id, "en",
                                 "Break of Structure (BOS)",
                                 content="## BOS Explained\nA break confirms trend continuation.\n\n### How to Trade\n1. Wait for break\n2. Wait for pullback\n3. Enter on confirmation")
                    upsert_trans("lesson_translations", "lesson_id", l.id, "ar",
                                 "كسر الهيكل (BOS)",
                                 content="## شرح BOS\nيؤكد الكسر استمرار الاتجاه.\n\n### كيفية التداول\n1. انتظر الكسر\n2. انتظر التراجع\n3. ادخل عند التأكيد")

        # M2: Order Blocks
        m2 = Module.query.filter_by(course_id=c1.id, order=2).first()
        if m2:
            upsert_trans("module_translations", "module_id", m2.id, "fr", "Order Blocks & FVG")
            upsert_trans("module_translations", "module_id", m2.id, "en", "Order Blocks & FVG")
            upsert_trans("module_translations", "module_id", m2.id, "ar", "كتل الأوامر والفجوات السعرية")

    # --- 2. PSYCHOLOGY COURSE ---
    c2 = Course.query.filter(Course.title.like("%Psychology%")).first()
    if c2:
        print(f"Translating Course: {c2.title}")
        upsert_trans("course_translations", "course_id", c2.id, "fr", 
                     "Mental de Fer : Psychologie", 
                     "Maîtrisez vos émotions, la peur et l'avidité.")
        upsert_trans("course_translations", "course_id", c2.id, "en", 
                     "Iron Mindset: Trading Psychology", 
                     "Conquer fear, greed, and emotional trading.")
        upsert_trans("course_translations", "course_id", c2.id, "ar", 
                     "عقلية حديدية: علم نفس التداول", 
                     "تغلب على الخوف والجشع والتداول العاطفي.")


    print("✅ Multilingual Seeding Complete!")

if __name__ == '__main__':
    with app.app_context():
        seed_translations()
