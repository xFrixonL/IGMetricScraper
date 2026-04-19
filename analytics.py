class AnalyticsEngine:
    def __init__(self, data):
        self.perfil = data.get("perfil", {})
        self.posts = data.get("posts", [])
        self.reels = data.get("reels", [])
        self.followers = self.perfil.get("followers", 0)

    def generate_report(self):
        if self.followers == 0 or (not self.posts and not self.reels):
            return "⚠️ Datos insuficientes."

        stats = {
            "engagement_rate_posts": self._calc_er(self.posts),
            "engagement_rate_reels": self._calc_er(self.reels),
            "avg_likes_posts": self._avg(self.posts, "likes"),
            "avg_likes_reels": self._avg(self.reels, "likes"),
            "avg_plays_reels": self._avg(self.reels, "plays"),
            "best_post": self._get_top(self.posts, "likes"),
            "best_reel": self._get_top(self.reels, "plays"),
            "ratio_posts": self._calc_specific_ratio(self.posts),
            "ratio_reels": self._calc_specific_ratio(self.reels)
        }
        
        self._print_report(stats)
        return stats

    def _calc_er(self, collection):
        if not collection: return 0
        total_interactions = sum((item.get("likes", 0) + item.get("comments", 0)) for item in collection)
        return (total_interactions / self.followers / len(collection)) * 100

    def _avg(self, collection, key):
        if not collection: return 0
        return sum(item.get(key, 0) for item in collection) / len(collection)

    def _get_top(self, collection, key):
        if not collection: return None
        return max(collection, key=lambda x: x.get(key, 0))

    def _calc_specific_ratio(self, collection):
        if not collection: return 0
        total_likes = sum(item.get("likes", 0) for item in collection)
        total_comments = sum(item.get("comments", 0) for item in collection)
        return (total_comments / total_likes) if total_likes > 0 else 0

    def _print_report(self, s):
        print(f"\n📊 RESUMEN ANALÍTICO: @{self.perfil.get('username')}")
        print("-" * 40)
        print(f"👥 Seguidores: {self.followers:,}")
        
        print(f"\n🖼️ SECCIÓN POSTS (Muestra: {len(self.posts)})")
        print(f"   📈 ER Promedio: {s['engagement_rate_posts']:.2f}%")
        print(f"   ❤️ Promedio Likes: {s['avg_likes_posts']:,.0f}")
        print(f"   💬 Ratio de Conversación: {s['ratio_posts']:.3f}")
        if s['best_post']:
            print(f"   🏆 Mejor Post: {s['best_post']['code']} ({s['best_post']['likes']:,} likes)")

        print(f"\n🎬 SECCIÓN REELS (Muestra: {len(self.reels)})")
        print(f"   📈 ER Promedio: {s['engagement_rate_reels']:.2f}%")
        print(f"   ▶️ Promedio Plays: {s['avg_plays_reels']:,.0f}")
        print(f"   ❤️ Promedio Likes: {s['avg_likes_reels']:,.0f}")
        print(f"   💬 Ratio de Conversación: {s['ratio_reels']:.3f}")
        if s['best_reel']:
            print(f"   🏆 Mejor Reel: {s['best_reel']['code']} ({s['best_reel']['plays']:,} plays)")
        
        print("-" * 40)