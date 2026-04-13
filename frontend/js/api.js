/**
 * API调用封装
 */

const API_BASE = 'http://127.0.0.1:5000/api';

// 当前登录用户
let currentUser = null;

// ========== 工具函数 ==========

function request(url, options = {}) {
    return fetch(API_BASE + url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    })
    .then(res => res.json())
    .then(data => {
        if (data.code !== 200) {
            console.warn('API请求失败:', data.message || url);
            return null;
        }
        return data.data;
    })
    .catch(err => {
        console.warn('网络错误，请检查后端服务是否启动:', err);
        return null;
    });
}

// ========== 认证相关 ==========

const Auth = {
    register(username, password, interests = []) {
        return request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, password, interests })
        });
    },

    login(username, password) {
        return request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },

    logout() {
        currentUser = null;
        localStorage.removeItem('user');
        return Promise.resolve();
    },

    getCurrentUser() {
        if (!currentUser) {
            const stored = localStorage.getItem('user');
            if (stored) {
                currentUser = JSON.parse(stored);
            }
        }
        return currentUser;
    },

    setCurrentUser(user) {
        currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));
    }
};

// ========== 景点相关 ==========

const Attractions = {
    // 获取景点列表
    list(params = {}) {
        const query = new URLSearchParams(params).toString();
        return request('/attractions' + (query ? '?' + query : ''));
    },

    // 获取单个景点
    get(id) {
        return request(`/attractions/${id}`);
    },

    // 搜索景点
    search(keyword, limit = 10) {
        return request(`/attractions/search?q=${encodeURIComponent(keyword)}&limit=${limit}`);
    },

    // 个性化推荐
    recommend(userId, limit = 10) {
        const params = new URLSearchParams({ limit });
        if (userId) params.append('user_id', userId);
        return request('/recommend?' + params.toString());
    },

    // 获取校园列表
    getCampuses() {
        return request('/campuses');
    }
};

// ========== 路线相关 ==========

const Routes = {
    // 最短路径
    shortest(from, to, options = {}) {
        return request('/route/shortest', {
            method: 'POST',
            body: JSON.stringify({
                from,
                to,
                campus_id: options.campus_id,
                transport: options.transport || '步行',
                weight: options.weight || 'distance'
            })
        });
    },

    // TSP多景点路线
    tsp(start, nodes, options = {}) {
        return request('/route/tsp', {
            method: 'POST',
            body: JSON.stringify({
                start,
                nodes,
                campus_id: options.campus_id,
                transport: options.transport || '步行',
                optimize: options.optimize !== false
            })
        });
    }
};

// ========== 场所相关 ==========

const Nearby = {
    // 附近设施
    search(x, y, range = 500, params = {}) {
        const query = new URLSearchParams({
            x, y, range,
            ...params
        }).toString();
        return request('/nearby?' + query);
    },

    // 设施列表
    list(params = {}) {
        const query = new URLSearchParams(params).toString();
        return request('/facilities' + (query ? '?' + query : ''));
    },

    // 设施类型
    getTypes() {
        return request('/facility-types');
    }
};

// ========== 日记相关 ==========

const Diaries = {
    // 日记列表
    list(params = {}) {
        const query = new URLSearchParams(params).toString();
        return request('/diaries' + (query ? '?' + query : ''));
    },

    // 获取单个日记
    get(id) {
        return request(`/diary/${id}`);
    },

    // 创建日记
    create(data) {
        return request('/diary', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // 更新日记
    update(id, data) {
        return request(`/diary/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    // 删除日记
    delete(id, userId) {
        return request(`/diary/${id}?user_id=${userId}`, {
            method: 'DELETE'
        });
    },

    // 搜索日记
    search(keyword, limit = 10) {
        return request(`/diaries/search?q=${encodeURIComponent(keyword)}&limit=${limit}`);
    },

    // 评分
    rate(id, rating) {
        return request(`/diary/${id}/rate`, {
            method: 'POST',
            body: JSON.stringify({ rating })
        });
    }
};

// ========== 美食相关 ==========

const Foods = {
    // 美食列表
    list(params = {}) {
        const query = new URLSearchParams(params).toString();
        return request('/foods' + (query ? '?' + query : ''));
    },

    // 搜索美食
    search(keyword, params = {}) {
        const query = new URLSearchParams({ q: keyword, ...params }).toString();
        return request('/foods/search?' + query);
    },

    // 推荐美食
    recommend(params = {}) {
        const query = new URLSearchParams(params).toString();
        return request('/foods/recommend?' + query);
    },

    // 获取菜系
    getCuisines() {
        return request('/cuisines');
    }
};

// ========== 用户相关 ==========

const User = {
    // 获取用户信息
    getProfile(userId) {
        return request(`/user/profile?user_id=${userId}`);
    },

    // 更新用户信息
    updateProfile(data) {
        return request('/user/profile', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    // 获取收藏
    getFavorites(userId) {
        return request(`/user/favorites?user_id=${userId}`);
    },

    // 添加收藏
    addFavorite(userId, attractionId) {
        return request('/user/favorites', {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, attraction_id: attractionId })
        });
    },

    // 取消收藏
    removeFavorite(userId, attractionId) {
        return request(`/user/favorites/${attractionId}?user_id=${userId}`, {
            method: 'DELETE'
        });
    },

    // 获取用户日记
    getDiaries(userId) {
        return request(`/user/diaries?user_id=${userId}`);
    }
};

// ========== AIGC相关 ==========

const AIGC = {
    generateAnimation(location, images = [], description = '') {
        return request('/aigc/animation', {
            method: 'POST',
            body: JSON.stringify({
                location,
                images,
                description
            })
        });
    }
};

// ========== 导出 ==========

window.API = {
    Auth,
    Attractions,
    Routes,
    Nearby,
    Diaries,
    Foods,
    User,
    AIGC
};
