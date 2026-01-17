import React, { useState } from 'react';
import { MessageCircle, Users, Share2, Heart, TrendingUp, Home, UserPlus, Calendar, Hash, Award, Image, Send, MoreHorizontal, UserCheck } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-hot-toast';


interface Post {
  id: string;
  author: {
    name: string;
    username: string;
    avatar: string;
    badge?: 'expert' | 'verified';
    profit?: string;
  };
  timestamp: string;
  content: string;
  asset?: string;
  hasImage?: boolean;
  likes: number;
  comments: number;
  shares: number;
  isLiked?: boolean;
}

interface TopTrader {
  id: string;
  name: string;
  username: string;
  avatar: string;
  profit: string;
  profitPercent: number;
}


const mockPosts: Post[] = [];

const topTraders: TopTrader[] = [
  {
    id: '1',
    name: 'Omar Benkirane',
    username: '@omar_pro',
    avatar: '🚀',
    profit: '+28.5%',
    profitPercent: 28.5
  },
  {
    id: '2',
    name: 'Fatima Zahra',
    username: '@fatima_trader',
    avatar: '💫',
    profit: '+19.2%',
    profitPercent: 19.2
  },
  {
    id: '3',
    name: 'Karim Hassani',
    username: '@karim_crypto',
    avatar: '🎯',
    profit: '+15.7%',
    profitPercent: 15.7
  }
];

const trendingTopics = [
  { tag: 'Bitcoin', count: '12 posts' },
  { tag: 'CasablancaStockExchange', count: '8 posts' },
  { tag: 'IAM', count: '5 posts' },
  { tag: 'ForexMaroc', count: '4 posts' },
  { tag: 'CryptoWhales', count: '3 posts' }
];

const Community: React.FC = () => {
  const { t } = useTranslation();
  const [activeMenu, setActiveMenu] = useState('feed');
  const [postText, setPostText] = useState('');
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [followedTraders, setFollowedTraders] = useState<string[]>([]);
  const [realTopTraders, setRealTopTraders] = useState<TopTrader[]>([]);
  const [allUsers, setAllUsers] = useState<any[]>([]);
  const [customGroups, setCustomGroups] = useState<any[]>([]);
  const [expandedPost, setExpandedPost] = useState<string | null>(null);
  const [postComments, setPostComments] = useState<Record<string, any[]>>({});
  const [commentText, setCommentText] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(true);

  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = React.useRef<HTMLInputElement>(null);


  React.useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      const token = localStorage.getItem('token');
      const headers: any = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      try {
        // 1. Fetch Top Traders for Sidebar
        const adminRes = await fetch('/api/admin/users', { headers: { 'X-ADMIN-KEY': 'TRADESENSE_SUPER_SECRET_2026' } });
        if (adminRes.ok) {
          const users = await adminRes.json();
          setAllUsers(users);
          const sorted = users.map((u: any) => ({
            id: u.user_id.toString(),
            name: u.name,
            username: '@' + u.email.split('@')[0],
            avatar: `https://ui-avatars.com/api/?name=${u.name}&background=random`,
            profit: u.challenges[0] ? `+${parseFloat(u.challenges[0].profit_percent).toFixed(1)}%` : '0%',
            rawProfit: u.challenges[0] ? u.challenges[0].equity - u.challenges[0].start_balance : 0
          })).sort((a: any, b: any) => b.rawProfit - a.rawProfit);
          setRealTopTraders(sorted.slice(0, 3));
        }

        // 2. Fetch Posts from NEW Endpoint
        const postsRes = await fetch('/api/community/posts', { headers });
        if (postsRes.ok) {
          const dbPosts = await postsRes.json();
          const formattedPosts: Post[] = dbPosts.map((p: any) => ({
            id: p.id.toString(),
            author: {
              name: p.author.name,
              username: '@' + p.author.username,
              avatar: p.author.avatar,
              profit: undefined, // Add if needed
              badge: undefined
            },
            timestamp: new Date(p.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            content: p.content,
            asset: p.tags ? p.tags.split(',')[0] : undefined,
            postImage: p.image_url ? `/api/community${p.image_url}` : undefined,
            likes: p.likes,
            comments: p.comments_count,
            shares: 0,
            isLiked: false
          }));
          setPosts(formattedPosts);
        }
      } catch (err) {
        console.error("Community Sync Error", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);


  const fetchComments = async (postId: string) => {
    const token = localStorage.getItem('token');
    const headers: any = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
      const res = await fetch(`/api/community/posts/${postId}/comments`, { headers });
      if (res.ok) {
        const comments = await res.json();
        // Map backend comment to frontend structure
        const mappedComments = comments.map((c: any) => ({
          user_name: c.author.name,
          user_avatar: c.author.avatar,
          content: c.content,
          timestamp: c.created_at
        }));
        setPostComments(prev => ({ ...prev, [postId]: mappedComments }));
      }
    } catch (err) {
      console.error("Comments fetch error", err);
    }
  };

  React.useEffect(() => {
    if (expandedPost) fetchComments(expandedPost);
  }, [expandedPost]);

  const handleLike = async (postId: string) => {
    const token = localStorage.getItem('token');
    if (!token) return toast.error('Veuillez vous connecter pour liker.');

    try {
      const res = await fetch(`/api/community/posts/${postId}/like`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setPosts(posts.map(p => p.id === postId ? { ...p, likes: data.count, isLiked: data.liked } : p));
      }
    } catch (err) { }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.size > 5 * 1024 * 1024) return toast.error('L\'image ne doit pas dépasser 5MB');

      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePublish = async () => {
    if (!postText.trim()) return;
    const token = localStorage.getItem('token');
    if (!token) return toast.error('Veuillez vous connecter pour publier.');

    const formData = new FormData();
    formData.append('content', postText);
    if (selectedAsset) formData.append('tags', selectedAsset);
    if (selectedImage) formData.append('image', selectedImage);

    try {
      const res = await fetch('/api/community/posts', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
          // Boundary handled automatically by browser
        },
        body: formData
      });

      if (res.ok) {
        const newPostData = await res.json();
        const newPost: Post = {
          id: newPostData.id.toString(),
          author: {
            name: newPostData.author.name,
            username: '@' + newPostData.author.username,
            avatar: newPostData.author.avatar
          },
          timestamp: 'Just now',
          content: newPostData.content,
          asset: newPostData.tags ? newPostData.tags.split(',')[0] : undefined,
          postImage: newPostData.image_url ? `/api/community${newPostData.image_url}` : undefined,
          likes: 0, comments: 0, shares: 0, isLiked: false
        };
        setPosts([newPost, ...posts]);
        setPostText('');
        setSelectedAsset(null);
        setSelectedImage(null);
        setImagePreview(null);
        toast.success('Post publié !');
      }
    } catch (err) {
      toast.error('Erreur lors de la publication');
    }
  };

  const handleAddComment = async (postId: string, text: string) => {
    if (!text.trim()) return;
    const token = localStorage.getItem('token');
    if (!token) return toast.error('Veuillez vous connecter.');

    try {
      const res = await fetch(`/api/community/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          content: text
        })
      });
      if (res.ok) {
        toast.success('Commentaire ajouté !');
        fetchComments(postId);
        setPosts(posts.map(p => p.id === postId ? { ...p, comments: p.comments + 1 } : p));
      }
    } catch (err) { }
  };

  const handleFollow = (traderId: string) => {
    if (followedTraders.includes(traderId)) {
      setFollowedTraders(followedTraders.filter(id => id !== traderId));
      toast.error('Désabonné');
    } else {
      setFollowedTraders([...followedTraders, traderId]);
      toast.success('Abonnement réussi !');
    }
  };

  const handleCreateGroup = () => {
    const groupName = window.prompt("Entrez le nom de votre nouveau groupe :");
    if (groupName && groupName.trim()) {
      const newGroup = {
        name: groupName.trim(),
        members: 1,
        color: 'bg-green-500',
        icon: groupName.charAt(0).toUpperCase()
      };
      setCustomGroups([newGroup, ...customGroups]);
      toast.success(`${t('community.groupJoined')} ${groupName}`);
    }
  };

  const handleInviteFriends = () => {
    const link = 'https://tradesense.ai/join/ref123';
    navigator.clipboard.writeText(link);
    toast.success('Lien d\'invitation copié ! Partagez-le avec vos amis.');
  };

  const renderContent = () => {
    switch (activeMenu) {
      case 'friends':
        return (
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="text-xl font-black text-gray-900 dark:text-white">{t('community.friends')}</h3>
                <p className="text-sm text-gray-500">{t('community.manageConnections')}</p>
              </div>
              <button
                onClick={handleInviteFriends}
                className="px-4 py-2 bg-yellow-500 text-black font-black rounded-lg hover:shadow-lg transition-all text-sm"
              >
                {t('community.inviteFriends')}
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {allUsers.length > 0 ? (
                allUsers.map((user: any) => (
                  <div key={user.user_id} className="bg-white dark:bg-white/5 p-4 rounded-xl border border-gray-200 dark:border-white/10 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-gray-200 dark:bg-white/10 rounded-full overflow-hidden">
                        <img src={`https://ui-avatars.com/api/?name=${user.name}&background=random`} alt={user.name} />
                      </div>
                      <div>
                        <p className="font-bold text-gray-900 dark:text-white">{user.name}</p>
                        <p className="text-xs text-gray-500">{t('common.traderProp')}</p>
                      </div>
                    </div>
                    <button
                      onClick={() => handleFollow(user.user_id.toString())}
                      className={`p-2 rounded-lg transition-all ${followedTraders.includes(user.user_id.toString()) ? 'bg-green-500/20 text-green-500' : 'bg-yellow-500 text-black'}`}
                    >
                      {followedTraders.includes(user.user_id.toString()) ? <UserCheck className="w-5 h-5" /> : <UserPlus className="w-5 h-5" />}
                    </button>
                  </div>
                ))
              ) : (
                <div className="col-span-2 py-20 text-center animate-pulse text-gray-400">
                  {t('community.loadingTraders')}
                </div>
              )}
            </div>
          </div>
        );
      case 'groups':
        return (
          <div className="p-8 text-center bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-white/10 m-6">
            <div className="w-20 h-20 bg-yellow-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <Users className="w-10 h-10 text-yellow-500" />
            </div>
            <h3 className="text-2xl font-black text-gray-900 dark:text-white mb-2">{t('community.groups')}</h3>
            <p className="text-gray-600 dark:text-gray-400 max-w-sm mx-auto mb-8">
              {t('community.discoverGroups')} Rejoignez des milliers de traders ou créez votre propre espace de discussion.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={handleCreateGroup}
                className="px-8 py-4 bg-yellow-500 text-black font-black rounded-2xl hover:shadow-2xl hover:-translate-y-1 transition-all flex items-center justify-center gap-2"
              >
                <UserPlus className="w-5 h-5" />
                {t('community.createGroup')}
              </button>
            </div>

            {customGroups.length > 0 && (
              <div className="mt-12 text-left">
                <h4 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-4">{t('community.createdGroups')}</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {customGroups.map((g, i) => (
                    <div key={i} className="p-4 bg-white/5 border border-white/10 rounded-2xl flex items-center gap-4">
                      <div className={`w-12 h-12 ${g.color} rounded-xl flex items-center justify-center text-white font-black text-xl`}>
                        {g.icon}
                      </div>
                      <div>
                        <p className="font-bold text-white">{g.name}</p>
                        <p className="text-xs text-gray-500">{g.members} {t('common.member')}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      case 'events':
        return (
          <div className="p-8 text-center">
            <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-black text-gray-900 dark:text-white mb-2">{t('community.events')}</h3>
            <p className="text-gray-600 dark:text-gray-400">{t('community.participateEvents')}</p>
            <button
              onClick={() => toast(t('community.nextEventMsg'), { icon: '📅' })}
              className="mt-4 px-6 py-3 bg-gradient-to-r from-yellow-400 to-yellow-600 text-black font-black rounded-xl hover:shadow-lg transition-all"
            >
              {t('community.viewEvents')}
            </button>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0b0e11]">
      <div className="max-w-[1600px] mx-auto flex">
        {/* Left Sidebar - Navigation */}
        <aside className="w-64 shrink-0 bg-white dark:bg-black/40 border-r border-gray-200 dark:border-white/10 h-screen sticky top-0 hidden lg:block">
          <div className="p-6">
            <h2 className="text-xl font-black text-gray-900 dark:text-white mb-6 flex items-center gap-2">
              <Users className="w-6 h-6 text-yellow-500" />
              {t('community.navigation')}
            </h2>

            {/* Main Menu */}
            <nav className="space-y-2 mb-8">
              {[
                { id: 'feed', icon: Home, label: t('community.feed') },
                { id: 'friends', icon: Users, label: t('community.friends') },
                { id: 'groups', icon: Users, label: t('community.groups') },
                { id: 'events', icon: Calendar, label: t('community.events') }
              ].map(item => (
                <button
                  key={item.id}
                  onClick={() => setActiveMenu(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-sm transition-all ${activeMenu === item.id
                    ? 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/5'
                    }`}
                >
                  <item.icon className="w-5 h-5" />
                  {item.label}
                </button>
              ))}
            </nav>

            {/* My Groups */}
            <div className="mt-8">
              <h3 className="text-xs font-black text-gray-500 dark:text-gray-600 uppercase tracking-wider mb-4 px-2">
                {t('community.myGroups')}
              </h3>
              <div className="space-y-2">
                {customGroups.length > 0 ? (
                  customGroups.map((group, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        toast.success(`${t('community.groupJoined')} ${group.name}`);
                        setActiveMenu('groups');
                      }}
                      className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-100 dark:hover:bg-white/5 transition-all text-left group"
                    >
                      <div className={`w-9 h-9 ${group.color} rounded-lg flex items-center justify-center text-white font-black text-xs shadow-lg group-hover:scale-110 transition-transform`}>
                        {group.icon}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-bold text-gray-900 dark:text-white truncate">{group.name}</p>
                        <p className="text-[10px] text-gray-500 dark:text-gray-600 font-bold uppercase tracking-tighter">
                          {group.members} {t('community.members')}
                        </p>
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="p-6 text-center bg-white/5 rounded-xl border border-white/10">
                    <Users className="w-8 h-8 text-gray-600 mx-auto mb-2" />
                    <p className="text-xs text-gray-500 font-medium">
                      Aucun groupe pour le moment
                    </p>
                    <button
                      onClick={handleCreateGroup}
                      className="mt-3 px-4 py-2 bg-yellow-500/10 text-yellow-500 text-xs font-bold rounded-lg hover:bg-yellow-500/20 transition-all"
                    >
                      Créer un groupe
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </aside>

        {/* Center Column - Main Feed */}
        <main className="flex-1 min-w-0 border-r border-gray-200 dark:border-white/10">
          <div className="max-w-[700px] mx-auto">
            {/* Header */}
            <div className="bg-white dark:bg-black/40 backdrop-blur-xl border-b border-gray-200 dark:border-white/10 p-6 sticky top-0 z-10">
              <h1 className="text-2xl font-black text-gray-900 dark:text-white mb-2">{t('community.title')}</h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {t('community.subtitle')}
              </p>
            </div>

            {/* Create Post Box */}
            <div className="p-4 bg-white dark:bg-black/40 border-b border-gray-200 dark:border-white/10">
              <div className="bg-gray-50 dark:bg-white/5 rounded-2xl border border-gray-200 dark:border-white/10 p-4">
                <div className="flex gap-3 mb-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center text-xl">
                    👤
                  </div>
                  <input
                    type="text"
                    value={postText}
                    onChange={(e) => setPostText(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handlePublish()}
                    placeholder={t('community.whatsYourStrategy')}
                    className="flex-1 bg-transparent text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-600 focus:outline-none font-medium"
                  />
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-white/10">
                  <div className="flex gap-2">
                    <button
                      onClick={() => setSelectedAsset(selectedAsset === 'BTC' ? null : 'BTC')}
                      className={`px-3 py-1.5 border rounded-lg font-black text-xs uppercase tracking-wider transition-all ${selectedAsset === 'BTC'
                        ? 'bg-orange-500 text-white border-orange-500'
                        : 'bg-orange-500/10 text-orange-500 border-orange-500/20 hover:bg-orange-500/20'
                        }`}
                    >
                      BTC
                    </button>
                    <button
                      onClick={() => setSelectedAsset(selectedAsset === 'GOLD' ? null : 'GOLD')}
                      className={`px-3 py-1.5 border rounded-lg font-black text-xs uppercase tracking-wider transition-all ${selectedAsset === 'GOLD'
                        ? 'bg-yellow-500 text-white border-yellow-500'
                        : 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20 hover:bg-yellow-500/20'
                        }`}
                    >
                      GOLD
                    </button>
                    <input
                      type="file"
                      ref={fileInputRef}
                      className="hidden"
                      accept="image/*"
                      onChange={handleImageSelect}
                    />
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="p-2 hover:bg-gray-100 dark:hover:bg-white/5 rounded-lg text-gray-500 transition-all"
                    >
                      <Image className="w-4 h-4" />
                    </button>
                  </div>
                  <button
                    onClick={handlePublish}
                    disabled={!postText.trim() && !selectedImage}
                    className="px-4 py-2 bg-gradient-to-r from-yellow-400 to-yellow-600 hover:from-yellow-500 hover:to-yellow-700 text-black font-black text-sm rounded-lg transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send className="w-4 h-4" />
                    {t('community.publish')}
                  </button>
                </div>

                {imagePreview && (
                  <div className="mt-4 relative inline-block">
                    <img src={imagePreview} alt="Preview" className="h-32 rounded-lg border border-gray-200 dark:border-white/10" />
                    <button
                      onClick={() => { setSelectedImage(null); setImagePreview(null); }}
                      className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md hover:bg-red-600 transition-colors"
                    >
                      <span className="sr-only">Remove</span>
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Posts Feed or Alternative Content */}
            {activeMenu === 'feed' ? (
              <div className="divide-y divide-gray-200 dark:divide-white/10">
                {posts.length > 0 ? (
                  posts.map((post) => (
                    <article
                      key={post.id}
                      className="p-4 bg-white dark:bg-black/40 hover:bg-gray-50 dark:hover:bg-white/5 transition-all"
                    >
                      {/* Post Header */}
                      <div className="flex items-start gap-3 mb-3">
                        <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-2xl shrink-0 overflow-hidden">
                          {post.author.avatar.startsWith('http') ? (
                            <img src={post.author.avatar} alt={post.author.name} className="w-full h-full object-cover" />
                          ) : (
                            post.author.avatar
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="font-black text-gray-900 dark:text-white">{post.author.name}</span>
                            {post.author.badge === 'expert' && (
                              <span className="px-2 py-0.5 bg-purple-500/20 text-purple-500 border border-purple-500/30 rounded-full text-xs font-black uppercase tracking-wider flex items-center gap-1">
                                <Award className="w-3 h-3" />
                                {t('community.expert')}
                              </span>
                            )}
                            {post.author.profit && (
                              <span className="px-2 py-0.5 bg-green-500/20 text-green-500 border border-green-500/30 rounded-full text-xs font-black">
                                {post.author.profit} {t('community.thisMonth')}
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-600">
                            <span>{post.author.username}</span>
                            <span>•</span>
                            <span>{post.timestamp}</span>
                          </div>
                        </div>
                        <button className="p-2 hover:bg-gray-200 dark:hover:bg-white/10 rounded-lg transition-all">
                          <MoreHorizontal className="w-5 h-5 text-gray-500 dark:text-gray-600" />
                        </button>
                      </div>

                      {/* Post Content */}
                      <div className="mb-4">
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed mb-3">
                          {post.content}
                        </p>
                        {post.postImage && (
                          <div className="rounded-xl overflow-hidden border border-gray-200 dark:border-white/10 mt-2">
                            <img src={post.postImage} alt="Post content" className="w-full h-auto max-h-96 object-cover" />
                          </div>
                        )}
                        {post.asset && (
                          <div className="mt-2">
                            <span className="inline-block px-3 py-1 bg-gray-100 dark:bg-white/5 rounded-full text-xs font-bold text-gray-500 border border-gray-200 dark:border-white/10">
                              #{post.asset}
                            </span>
                          </div>
                        )}
                      </div>

                      {/* Post Actions */}
                      <div className="flex items-center gap-6 ml-[60px] pt-3 border-t border-gray-200 dark:border-white/10">
                        <button
                          onClick={() => handleLike(post.id)}
                          className={`flex items-center gap-2 transition-all ${post.isLiked
                            ? 'text-red-500 hover:text-red-600'
                            : 'text-gray-500 dark:text-gray-600 hover:text-red-500'
                            }`}
                        >
                          <Heart className={`w-5 h-5 ${post.isLiked ? 'fill-current' : ''}`} />
                          <span className="text-sm font-bold">{post.likes}</span>
                        </button>
                        <button
                          onClick={() => setExpandedPost(expandedPost === post.id ? null : post.id)}
                          className={`flex items-center gap-2 transition-all ${expandedPost === post.id ? 'text-blue-500' : 'text-gray-500 dark:text-gray-600 hover:text-blue-500'}`}
                        >
                          <MessageCircle className="w-5 h-5" />
                          <span className="text-sm font-bold">{post.comments}</span>
                        </button>
                        <button className="flex items-center gap-2 text-gray-500 dark:text-gray-600 hover:text-green-500 transition-all">
                          <Share2 className="w-5 h-5" />
                          <span className="text-sm font-bold">{post.shares}</span>
                        </button>
                      </div>

                      {/* Interactive Comment Section */}
                      {expandedPost === post.id && (
                        <div className="ml-[60px] mt-4 p-4 bg-gray-50 dark:bg-white/5 rounded-2xl border border-gray-200 dark:border-white/10 animate-in slide-in-from-top-2 duration-300">
                          <div className="flex gap-3 mb-4">
                            <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center text-xs text-black font-black">
                              MOI
                            </div>
                            <div className="flex-1 flex gap-2">
                              <input
                                type="text"
                                placeholder="Écrivez un commentaire..."
                                className="flex-1 bg-white dark:bg-black/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-yellow-500"
                                value={commentText[post.id] || ''}
                                onChange={(e) => setCommentText({ ...commentText, [post.id]: e.target.value })}
                                onKeyDown={(e) => {
                                  if (e.key === 'Enter') {
                                    handleAddComment(post.id, commentText[post.id]);
                                    setCommentText({ ...commentText, [post.id]: '' });
                                  }
                                }}
                              />
                              <button
                                onClick={() => {
                                  handleAddComment(post.id, commentText[post.id]);
                                  setCommentText({ ...commentText, [post.id]: '' });
                                }}
                                disabled={!commentText[post.id]?.trim()}
                                className="p-2 bg-yellow-500 rounded-lg text-black disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <Send className="w-4 h-4" />
                              </button>
                            </div>
                          </div>

                          <div className="space-y-3">
                            {(postComments[post.id] || []).map((c: any, i: number) => (
                              <div key={i} className="flex gap-3 items-start p-2 rounded-lg hover:bg-black/5 dark:hover:bg-white/5 transition-all">
                                <div className="w-8 h-8 bg-gray-300 dark:bg-white/10 rounded-full flex items-center justify-center overflow-hidden">
                                  <img src={c.user_avatar} alt={c.user_name} className="w-full h-full object-cover" />
                                </div>
                                <div>
                                  <p className="text-sm">
                                    <span className="font-bold text-gray-900 dark:text-white mr-2">{c.user_name}</span>
                                    <span className="text-gray-600 dark:text-gray-400">{c.content}</span>
                                  </p>
                                  <p className="text-[10px] text-gray-500 mt-1">{new Date(c.timestamp).toLocaleTimeString()}</p>
                                </div>
                              </div>
                            ))}
                            {(postComments[post.id] || []).length === 0 && (
                              <p className="text-center text-xs text-gray-500 py-4 italic">Aucun commentaire pour le moment.</p>
                            )}
                          </div>
                        </div>
                      )}
                    </article>
                  ))) : (
                  <div className="p-20 text-center text-gray-500 italic">
                    {!isLoading ? 'Le flux est vide. Soyez le premier à publier !' : 'Chargement...'}
                  </div>
                )}
                {isLoading && posts.length > 0 && (
                  <div className="p-4 text-center text-gray-400 text-sm">Chargement...</div>
                )}
              </div>
            ) : (
              renderContent()
            )}
          </div>
        </main>

        {/* Right Sidebar - Suggestions */}
        <aside className="w-80 shrink-0 bg-white dark:bg-black/40 h-screen sticky top-0 overflow-y-auto hidden xl:block">
          <div className="p-6 space-y-6">
            {/* Top Traders */}
            <div className="bg-gray-50 dark:bg-white/5 rounded-2xl border border-gray-200 dark:border-white/10 p-4">
              <h3 className="text-lg font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-yellow-500" />
                {t('community.topTraders')}
              </h3>
              <div className="space-y-3">
                {(realTopTraders.length > 0 ? realTopTraders : topTraders).map((trader) => (
                  <div key={trader.id} className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center text-xl shrink-0 overflow-hidden">
                      {trader.avatar.startsWith('http') ? (
                        <img src={trader.avatar} alt={trader.name} className="w-full h-full object-cover" />
                      ) : (
                        trader.avatar
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-bold text-gray-900 dark:text-white text-sm truncate">{trader.name}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-600">{trader.username}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-black text-green-500">{trader.profit}</p>
                      <button
                        onClick={() => handleFollow(trader.id)}
                        className={`text-xs font-bold transition-all ${followedTraders.includes(trader.id)
                          ? 'text-gray-500 hover:text-gray-600'
                          : 'text-blue-500 hover:text-blue-600'
                          }`}
                      >
                        {followedTraders.includes(trader.id) ? t('community.following') : t('community.follow')}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Trending Topics */}
            <div className="bg-gray-50 dark:bg-white/5 rounded-2xl border border-gray-200 dark:border-white/10 p-4">
              <h3 className="text-lg font-black text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Hash className="w-5 h-5 text-yellow-500" />
                {t('community.trendingTopics')}
              </h3>
              <div className="space-y-3">
                {trendingTopics.map((topic, idx) => (
                  <button
                    key={idx}
                    className="w-full text-left hover:bg-gray-100 dark:hover:bg-white/5 rounded-lg p-2 transition-all"
                  >
                    <p className="font-bold text-gray-900 dark:text-white text-sm flex items-center gap-1">
                      <Hash className="w-4 h-4 text-gray-500 dark:text-gray-600" />
                      {topic.tag}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-600 ml-5">{topic.count}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default Community;
