from datetime import datetime

class ProfileProcessor:
    def __init__(self, target_username):
        self.target_username = target_username.lower()
        self.profile_info = {}
        self.posts = []
        self.reels = []
        self.scrape_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_identity(self, data):
        user = data.get("data", {}).get("user", {})
        if user:
            username = user.get("username", "").lower()
            if username == self.target_username:
                self.profile_info = {
                    "username": user.get("username"),
                    "full_name": user.get("full_name"),
                    "followers": user.get("follower_count", 0),
                    "following": user.get("following_count", 0),
                    "biography": user.get("biography"),
                    "is_verified": user.get("is_verified", False),
                    "posts_count": user.get("media_count", 0),
                    "scrape_date": self.scrape_date
                }
                print(f"✅ Perfil detectado: @{self.profile_info.get('username')}")
            else:
                pass

    def process_feed_posts(self, data):
        edges = data.get("data", {}).get("xdt_api__v1__feed__user_timeline_graphql_connection", {}).get("edges", [])
        for edge in edges:
            node = edge.get("node", {})
            if node.get("product_type") == "clips" or len(self.posts) >= 10:
                continue
            
            code = node.get("code")
            if code and not any(p['code'] == code for p in self.posts):
                self.posts.append({
                    "code": code,
                    "type": node.get("product_type"),
                    "taken_at": self.format_date(node.get("taken_at")),
                    "likes": node.get("like_count") or node.get("edge_media_preview_like", {}).get("count", 0),
                    "comments": node.get("comment_count") or node.get("edge_media_to_comment", {}).get("count", 0)
                })

    def process_reels_connection(self, data):
        """Procesa el query masivo de la pestaña /reels/"""
        connection = data.get("data", {}).get("xdt_api__v1__clips__user__connection_v2", {})
        edges = connection.get("edges", [])
        for edge in edges:
            if len(self.reels) >= 10: break
            node = edge.get("node", {}).get("media", {})
            code = node.get("code")
            if code and not any(r['code'] == code for r in self.reels):
                self.reels.append(self._extract_reel_data(node))

    def process_reel_info(self, data):
        """Procesa el JSON individual de info/ al abrir un modal"""
        items = data.get("items", [])
        if items:
            item = items[0]
            code = item.get("code")
            new_data = self._extract_reel_data(item)
            
            for i, reel in enumerate(self.reels):
                if reel["code"] == code:
                    self.reels[i].update(new_data)
                    print(f"   ✅ Data actualizada (modal) para reel: {code}")
                    return
            
            if len(self.reels) < 10:
                self.reels.append(new_data)

    def _extract_reel_data(self, item):
        return {
            "code": item.get("code"),
            "taken_at": self.format_date(item.get("taken_at")),
            "likes": item.get("like_count", 0),
            "comments": item.get("comment_count", 0),
            "plays": item.get("play_count") or item.get("view_count", 0),
            "duration": item.get("video_duration", 0)
        }

    def format_date(self, timestamp):
        if not timestamp: return None
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")