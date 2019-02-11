#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# 参考https://github.com/Vespa314/bilibili-api/blob/master/api.md
import os
import sys
import aiohttp
import aiofiles
import asyncio
import chardet  # 检测编码格式
import requests
import threading
import subprocess
import xml.dom.minidom
from util import *
from tqdm import tqdm
from contextlib import closing
from multiprocessing import cpu_count
from danmuku2ass import Danmaku2ASS, ConvertColor


signApiUrl = "https://interface.bilibili.com/v2/playurl?"
apiUrl = 'https://api.bilibili.com/x/'  # API地址
webApiPrefix = apiUrl + 'web-interface/'  # web API前缀
playerApiPrefix = apiUrl + 'player/'  # player API前缀
spaceApiPrefix = apiUrl + 'space/'  # space API前缀
relationApiPrefix = apiUrl + 'relation/'  # relation API前缀
searchApiPrefix = webApiPrefix + 'search/'  # search API前缀

allSearchUrl = searchApiPrefix + 'all?keyword={0}&page={1}'  # 视频全局搜索，需要关键词
typeSearchUrl = searchApiPrefix + 'type?keyword={0}&page={1}&search_type={2}&highlight={3}'  # 视频指定类型搜索，需要关键词


class Search:
    @staticmethod
    @exec_time
    def search_all(keyword, page=1):
        """
        全局搜索
        :param keyword: 关键词
        :param page: 页码
        :return:

        API返回示例：
        {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": {
            "seid": "11777069692255910012",
            "page": 2,  页码
            "pagesize": 20,  每页数据
            "numResults": 1000,  结果总数
            "numPages": 50,  总页数
            "suggest_keyword": "",  建议搜索词
            "rqt_type": "search",
            "cost_time": {  搜索花费时间
                "params_check": "0.000483",
                "illegal_handler": "0.000090",
                "as_response_format": "0.004703",
                "mysql_request": "0.0000510.000048",
                "as_request": "0.107378",
                "save_cache": "0.000646",
                "as_request_format": "0.001677",
                "deserialize_response": "0.000391",
                "total": "0.115821",
                "main_handler": "0.114490"
            },
            "exp_list": {
                "5511": true,
                "6614": true
            },
            "egg_hit": 0,
            "pageinfo": {  搜索页统计信息
                "pgc": {  影视栏
                    "numResults": 0, 搜索结果数
                    "total": 0,  总共结果数
                    "pages": 0   总页数
                },
                "live_room": {},  直播间
                "photo": {},  相簿栏
                "topic": {},  话题栏
                "video": {},  视频栏
                "user": {},
                "bili_user": {}, 用于综合搜索结果显示用户类
                "media_ft": {},  用于综合搜索结果显示的影视类
                "article": {},  专题栏
                "media_bangumi": {},  用于综合搜索结果显示的番剧类
                "special": {},
                "operation_card": {},
                "upuser": {},  用户栏
                "movie": {},
                "live_all": {},
                "tv": {},
                "live": {},  直播栏
                "card": {},
                "bangumi": {},  番剧栏
                "activity": {},  用于综合搜索结果显示活动类
                "live_master": {},
                "live_user": {}
            },
            "result": {
                "star": [],
                "operation_card": [],
                "twitter": [],
                "tv": [],
                "live_room": [],
                "bili_user": [{  用户
                        "rank_offset": 1,
                        "usign": "",  用户签名
                        "videos": 1215,  投稿数
                        "fans": 848347,  粉丝数
                        "is_upuser": 1,
                        "upic": "",  用户头像
                        "uname": "",  用户名
                        "official_verify": {  认证账号
                            "type": 1,  认证类型，1为机构认证
                            "desc": ""  认证描述
                        },
                        "verify_info": "",
                        "rank_score": 1000000000,
                        "level": 6,  用户等级
                        "gender": 2,  用户性别，1为男，2为女
                        "hit_columns": [],
                        "mid": 178778949,  用户ID
                        "is_live": 0,  是否在线
                        "room_id": 5472071,  直播间ID
                        "res": [{  投稿稿件信息，一般是3个
                                "play": "21487",  播放次数
                                "dm": 54,  稿件弹幕数
                                "pubdate": 1548147616,  稿件上传时间
                                "title": "",  稿件标题
                                "pic": "",  稿件封面地址
                                "fav": 19,  稿件收藏数
                                "is_union_video": 0,
                                "is_pay": 0,
                                "duration": "1:58",  稿件时长（分：秒）
                                "aid": 41375404,  稿件ID
                                "coin": 49,  稿件硬币数
                                "arcurl": "",  稿件地址
                                "desc": ""  稿件描述
                            }, ...
                        ],
                        "rank_index": 0,
                        "type": "bili_user"  类型，目前固定为‘bili_user’
                    }

                ],
                "activity": [{
                        "status": 1,  状态
                        "author": "",  作者
                        "url": "",  活动地址
                        "country": null,  国家
                        "title": "",  标题
                        "cover": "",  封面地址
                        "pos": 1,
                        "state": 1,
                        "corner": "", 目前发现固定为‘活动’
                        "type": "activity",  类型
                        "id": 156,
                        "desc": ""  描述
                    }, ...
                ],
                "topic": [],
                "tag": [],
                "video": [{  视频信息
                        "new_rec_tags": [],
                        "pubdate": 1547274509,  上传时间
                        "rank_offset": 21,  排行
                        "tag": "",  UP自定义视频标签
                        "duration": "3:37",  视频时长（分：秒）
                        "id": 40539042,  视频AV号
                        "rank_score": 101282899,
                        "badgepay": false,
                        "senddate": 1547318659,
                        "title": "",  视频标题
                        "review": 79,  视频评论数
                        "mid": 238093337,  UP主ID
                        "is_union_video": 0,
                        "rank_index": 0,
                        "type": "video",  视频类型，目前固定为‘video’
                        "arcrank": "0",
                        "play": 11883,  视频播放数
                        "pic": "",  视频封面地址
                        "description": "",  视频简介
                        "view_type": "",
                        "video_review": 75,  视频弹幕数
                        "is_pay": 0,
                        "favorites": 355,  视频收藏数
                        "arcurl": "",  视频地址
                        "typeid": "130",  视频分类ID
                        "author": "",  视频作者
                        "hit_columns": ["title", "description"],  搜索时命中范围
                        "typename": "",  视频分类名
                        "aid": 40539042,  视频AV号
                        "rec_tags": null
                    }, ...
                ],
                "card": [],
                "article": [],
                "media_ft": [],
                "comic": [],
                "media_bangumi": [{  番剧信息
                        "styles": "",  番剧风格
                        "all_net_url": "",
                        "media_id": 5616,  番剧ID
                        "hit_columns": ["org_title"],  搜索时命中范围
                        "rank_offset": 1,
                        "all_net_name": "",
                        "season_id": 5616,
                        "display_info": [{
                                "bg_color_night": "#BB5B76",
                                "text": "会员抢先",
                                "border_color": "#FB7299",  text的背景色
                                "bg_style": 1,
                                "text_color": "#FFFFFF",  text的颜色
                                "bg_color": "#FB7299",  标题字体颜色
                                "text_color_night": "#E5E5E5",  番剧介绍字体颜色
                                "border_color_night": "#BB5B76"
                            }
                        ],
                        "goto_url": "",  番剧播放页地址
                        "media_score": {  番剧评分
                            "user_count": 39914,  点评人数
                            "score": 9.4  得分
                        },
                        "corner": 2,
                        "desc": "",  番剧简介
                        "rank_index": 0,
                        "cv": "",  番剧声优
                        "areas": "",  番剧地区
                        "is_avid": false,
                        "title": "",  番剧名
                        "org_title": "",  番剧原名
                        "cover": "",  番剧封面地址
                        "angle_title": "会员抢先",
                        "fix_pubtime_str": "",
                        "media_mode": 2,
                        "play_state": 0,
                        "angle_color": 0,
                        "all_net_icon": "",
                        "media_type": 1,
                        "rank_score": 773510027,
                        "staff": "",  番剧职员表
                        "type": "media_bangumi",  番剧类型，目前固定为‘media_bangumi’
                        "pubtime": 1538841600  番剧第一发布时间
                    }, ...
                ],
                "special": [],
                "user": []
            },
            "top_tlist": {  分栏统计数据条数
                "pgc": 0,
                "live_room": 3,  直播间
                "photo": 1000,  相簿栏
                "topic": 3,  话题栏
                "video": 1000,  视频栏
                "user": 0,
                "bili_user": 1000,  用户栏
                "media_ft": 0,
                "article": 1000,  专题栏
                "media_bangumi": 8,  番剧栏
                "card": 0,
                "operation_card": 0,
                "upuser": 0,
                "movie": 0,
                "tv": 0,
                "live": 3, 直播间
                "special": 58,
                "bangumi": 0,
                "activity": 1, 活动
                "live_master": 0,
                "live_user": 1000  用户
            },
            "show_column": 0
        }
    }
        """
        key = get_keyword(keyword)
        url = allSearchUrl.format(key, page)
        json_info = get_json_info(url)
        data = json_info.get_value('data')
        return data

    @staticmethod
    @exec_time
    def search_type(keyword, page=1, search_type='video', highlight=1, **kwargs):
        """
        视频类型搜索
        :param keyword: 关键词
        :param page: 页码
        :param search_type: 搜索类型
        :param highlight: 是否高亮
        :param kwargs 可选参数，根据搜索类型的不同而有所不同
        :return:

        search_type参数：
        video:视频
        media_bangumi：番剧
        media_ft:影视
        live：直播，包括主播和直播间
        live_user：直播主播
        article：专栏文章
        topic：话题
        bili_user:用户（目前支持搜索UP主、Lv2及以上绑定手机的大部分用户）
        photo:相簿

        kwargs参数(默认情况下，order=totalrank，duration=0，tid=0，category_id=0)：
        order：排序依据(video，article，bili_user类型支持)
        duration：持续时间范围(video类型支持)
        tids：分区ID(video类型支持)
        category_id：分区ID(article，photo类型支持)
        order_sort：排序顺序，与order配合使用(bili_user类型支持)
        user_type:用户类型(bili_user类型支持)

        order参数：
        totalrank：综合排序（默认值）（video，article，photo类型支持）
        pubdate：最新发布（从新到老）（video，article，photo类型支持）
        click：最多点击（从多到少）（video，article类型支持）
        stow：最多收藏（从多到少）(video，photo类型支持)
        dm：最多弹幕（从多到少）(video类型支持)
        attention：最多喜欢（根据rank_score从大到小）(article类型支持)
        scores：最多评论（根据评论数从多到少）(article类型支持)

        0：默认排序，order_sort=0(bili_user类型支持)
        fans：粉丝数排序，order_sort=0：由高到低，order_sort=1：由低到高(bili_user类型支持)
        level:Lv等级排序，order_sort=0：由高到低，order_sort=1：由低到高(bili_user类型支持)

        user_type参数：
        0：全部用户
        1：UP主
        2：普通用户
        3：认证用户

        duration参数：
        0：全部（默认）
        1:10分钟以下
        2:10-30分钟
        3:30-60分钟
        4:60分钟以上

        category_id参数（默认为0表示全部分区，video，photo类型支持）：
        游戏：1(video类型支持)
        动画：2(video类型支持)
        生活：3(video类型支持)
        轻小说：16(video类型支持)
        科技：17(video类型支持)
        影视：28(video类型支持)
        兴趣：29(video类型支持)

        画友：1(photo类型支持)
        摄影：2(photo类型支持)

        tids参数（0表示对所有B站分区进行搜索）：
        综合排名：0
        动画：1
            AMD·AMV：24
            MMD·3D：25
            原创·配音：47
                原创：48
                中配：49
            二次元鬼畜：26
            综合：27
                手书：50
                咨询：51
                杂谈：52
                其他：53
        音乐/舞蹈：3
            音乐视频：28
                OP/ED：54
                其他：55
            Vocaloid相关：30
                Vocaloid：56
                UTAU相关：57
                中文曲：58
            翻唱：31
            舞蹈：20
            演奏：59
            三次元音乐：29
        游戏：4
            游戏视频：17
                预告·演示：61
                其他：63
            游戏攻略·解说：18
                单机游戏：64
                网络游戏：65
                家用·掌机：66
                其他：67
            Mugen：19
            电子竞技：60
                赛事：68
                解说：69
                其它：70
        科学技术:36
            全球科技：39
                数码科技：95
                军事科技：96
                手机测评：97
                其它：98
            科普·人文：37
                BBC纪录片：99
                探索频道：100
                国家地理：101
                NHK：102
                TED演讲：103
                名校公开课：104
                教程·演示：105
                其它：107
            野生技术协会：40
            趣味短片·其它：108
        娱乐：5
            生活娱乐：21
            三次元鬼畜：22
            动物圈：75
                喵星人：77
                汪星人：78
                其它：79
            美食：76
                美食视频：80
                制作教程：81
            综艺：71
        影视：11
            连载剧集：15
                国产：110
                日剧：111
                美剧：112
                其它：113
            完结剧集：34
                国产：87
                日剧：88
                美剧：89
                其它：90
            电影：23
                预告·花絮：82
                电影：83
            微电影：85
            特摄·布袋：86
                特摄：91
                布袋戏：92
        动漫剧番：13
            连载动画：33
            完结动画：32
            剧场·OVA：94

        注意：搜索的数据每页固定20条数据，最多只有1000条，也就是50页
        """
        key = get_keyword(keyword)
        url = typeSearchUrl.format(key, page, search_type, highlight)
        string = get_search_string(kwargs)
        if string:
            url += '&' + string
        json_info = get_json_info(url)
        data = json_info.get_value('data')
        return data


class User:
    userSpaceInfoUrl = spaceApiPrefix + 'acc/info?mid={}'  # 指定mid(用户id)空间信息，根据空间主人设置得到相应信息
    userTopVideoInfoUrl = spaceApiPrefix + 'top/arc?vmid={}'  # 用户空间置顶视频信息，需要mid(用户id)
    userCoinVideoUrl = spaceApiPrefix + 'coin/video?vmid={}'  # 用户投币视频信息，需要mid(用户id)
    userChannelListInfoUrl = spaceApiPrefix + 'channel/list?mid={}'  # 用户频道投稿列表，需要mid(用户id)
    userArticleListInfoUrl = spaceApiPrefix + 'article?mid={}'  # 用户专栏投稿列表，需要mid(用户id)
    userFansListInfoUrl = relationApiPrefix + 'followers?vmid={0}&pn={1}&ps=50&order=desc'  # 用户粉丝列表，需要mid(用户id)，限制访问前5页，每页最多50条数据
    userFollowListInfoUrl = relationApiPrefix + 'followings?vmid={0}&pn={1}&ps=50&order=desc'  # 用户关注列表，需要mid(用户id)，限制访问前5页，每页最多50条数据

    # 用户订阅番剧信息，需要mid(用户id)，每页固定15条数据
    userBangumiInfoUrl = 'https://space.bilibili.com/ajax/Bangumi/getList?mid={}'
    # 用户视频投稿信息，需要mid(用户id),单页限制100条数据，超过会报参数错误
    userSubmitInfoUrl = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=30&order=pubdate'
    # 用户直播间信息，需要mid(用户id)
    userLivingInfoUrl = 'https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={}'
    # 用户音频投稿列表，需要mid(用户id),不更改页数时，单页限制100条数据，超过JSON格式会发生变化
    userAudioListInfoUrl = 'https://api.bilibili.com/audio/music-service/web/song/upper?uid={}&pn=1&ps=30&order=1'
    # 用户相簿数目信息，需要mid(用户id)
    userLinkDrawCountInfoUrl = 'https://api.vc.bilibili.com/link_draw/v1/doc/upload_count?uid={}'
    # 用户相簿列表信息，需要mid(用户id),不更改页数时，单页限制100条数据，超过JSON格式会发生变化
    userLinkDrawListInfoUrl = 'https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid={}&page_num=0&page_size=30&biz=all'

    userInfoUrl = webApiPrefix + 'nav'  # 用户信息，需要登录，最详细
    userInfoUrl1 = spaceApiPrefix + 'myinfo'  # 用户信息，需要登录，较详细
    userInfoUrl2 = 'https://account.bilibili.com/home/userInfo'  # 用户信息，需要登录，较详细
    userInfoUrl3 = 'https://api.bilibili.com/x/member/web/account'  # 用户信息，需要登录，简略信息
    userVipInfoUrl = 'https://big.bilibili.com/web/user/info'  # 用户大会员信息，需要登录
    userIdentifyInfoUrl = 'https://account.bilibili.com/identify/index'  # 用户认证信息，需要登录
    userUnreadMsgUrl = 'https://api.vc.bilibili.com/web_im/v1/web_im/unread_msgs'  # 未读消息的相关信息，需要登录
    userNotifyCountUrl = 'https://message.bilibili.com/api/notify/query.notify.count.do'  # 消息中各个类型信息的个数，需要登录

    def __init__(self, mid):
        self.mid = mid
        self.name = ''  # 用户名
        self.official = False  # 是否是认证账号
        self.official_title = ''  # 认证用户的认证标题
        self.official_description = ''  # 认证用户的认证描述
        self.sex = ''  # 用户性别
        self.avatar = ''  # 用户头像地址
        self.sign = ''  # 用户签名
        self.level = 0  # 用户等级
        self.create_time = 0  # 用户注册时间，unix时间戳
        self.birthday = ''  # 用户生日
        self.coins = 0  # 用户硬币数
        self.fans_badge = False  # 是否开通专属粉丝勋章
        self.top_photo = ''  # 空间头图
        self.vip = False  # 是否是会员
        self.vip_type = ''  # 会员类型
        self.fans_count = 0  # 粉丝总数
        self.fans_list = []  # 粉丝列表，从API最多得到250条数据
        self.follow_count = 0  # 关注总数
        self.follow_list = []  # 关注列表，从API最多得到250条数据

        # # 未赋值和使用
        # self.follow = None  # 关注好友数目
        # self.fans = None  # 粉丝数目
        # self.follow_list = None  # 关注列表
        # self.article = None  # 投稿数
        # self.place = None  # 所在地
        # self.message = None  # 承包时会返回的承保信息
        # self.friend = None
        # self.DisplayRank = None
        # self.rank = None
        # self.spaceName = None

        self.get_user_space_info()

        # self.get_user_fans_list()

        # self.get_user_follow_list()

    def __getattr__(self, name):  # 定义当用户试图获取一个不存在的属性时的行为
        return None

    def __str__(self):  # 定义当被str()调用或者打印对象时的行为
        return str(self.__dict__)  # 返回当前范围（类或实例）的所有属性名称列表

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    @staticmethod
    def get_vip_type(vip_type):
        type_int = int(vip_type)
        if type_int == 1:
            return '大会员'
        elif type_int == 2:
            return '年度大会员'
        else:
            return None

    def get_user_fans_list(self):
        """
        获取用户粉丝列表
        :return: None

        API返回示例：
        {
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data": {
                "list": [{
                        "mid": 5060603,
                        "attribute": 0,
                        "mtime": 1548081181,
                        "tag": null,
                        "special": 0,
                        "uname": "嘛达哦吉桑",
                        "face": "http://i0.hdslb.com/bfs/face/60a900657feee8309d40caa6a28a7155ba091598.gif",
                        "sign": "",
                        "official_verify": {
                            "type": -1,
                            "desc": ""
                        },
                        "vip": {
                            "vipType": 0,
                            "vipDueDate": 0,
                            "dueRemark": "",
                            "accessStatus": 0,
                            "vipStatus": 0,
                            "vipStatusWarn": ""
                        }
                    }, ...
                ],
                "re_version": 2009597532,
                "total": 834423
            }
        }
        """
        for i in range(1, 6):
            url = self.userFansListInfoUrl.format(self.mid, i)
            json_info = get_json_info(url)
            data = json_info.get_value('data')
            self.fans_count = data['total']
            self.fans_list = self.fans_list + data['list']

    def get_user_follow_list(self):
        """
        获取用户关注列表
        :return: None

        API返回示例：
        {
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data": {
                "list": [{
                        "mid": 66994455,
                        "attribute": 0,
                        "mtime": 1546793955,
                        "tag": null,
                        "special": 0,
                        "uname": "绘恋制作组",
                        "face": "http://i0.hdslb.com/bfs/face/c3f6ad53a457ca06ef6c219fc95c3e4833b30f71.jpg",
                        "sign": "国产校园三角恋爱AVG《三色绘恋》官方哔哩哔哩账号",
                        "official_verify": {
                            "type": -1,
                            "desc": ""
                        },
                        "vip": {
                            "vipType": 0,
                            "vipDueDate": 0,
                            "dueRemark": "",
                            "accessStatus": 0,
                            "vipStatus": 0,
                            "vipStatusWarn": ""
                        }
                    }, ...
                ],
                "re_version": 144062522,
                "total": 48
            }
        }
        """
        for i in range(1, 6):
            url = self.userFollowListInfoUrl.format(self.mid, i)
            json_info = get_json_info(url)
            data = json_info.get_value('data')
            self.follow_count = data['total']
            self.follow_list = self.follow_list + data['list']

    def get_user_space_info(self):
        """
        用户空间信息
        :return None

        API返回示例：
        {
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data": {
                "mid": 19044889,
                "name": "pc迷你猪",  # 用户名
                "sex": "男",  # 性别
                "face": "http://i2.hdslb.com/bfs/face/c8eaab28e4c057c1f172e604c93c74ff6c23040b.jpg",  # 头像地址
                "sign": "黑枪不怪我的~坦克打不到我的~ q群：894531604",  # 签名
                "rank": 10000,
                "level": 6,  # 用户等级
                "jointime": 1449159501,  # 用户注册时间
                "moral": 0,
                "silence": 0,
                "birthday": "09-18",  # 用户生日
                "coins": 10943.4,  # 用户硬币数
                "fans_badge": false,  # 是否开通专属粉丝勋章
                "official": {  # B站认证
                    "role": 0,  # 认证类型，1为个人认证（中国），2为个人认证（外国），3为机构认证
                    "title": "",  # 认证标题
                    "desc": ""  # 认证描述
                },
                "vip": {
                    "type": 2,  # 会员类型，1为大会员，2为年度大会员
                    "status": 1 # 会员状态，1为激活
                },
                "is_followed": false,  # 自己是否是这个用户的粉丝，需登录才能得到正确信息，默认为false
                "top_photo": "http://i1.hdslb.com/bfs/space/265ecddc52d74e624dc38cf0cff13317085aedf7.png",  # 空间头图地址
                "theme": {}
            }
        }
        """
        url = self.userSpaceInfoUrl.format(self.mid)
        json_info = get_json_info(url)
        data = json_info.get_value('data')
        self.name = data['name']
        self.official = int(data['official']['role']) != 0
        self.official_title = data['official']['title']
        self.official_description = data['official']['desc']
        self.sex = data['sex']
        self.avatar = data['face']
        self.sign = data['sign']
        self.level = data['level']
        self.create_time = data['jointime']
        self.birthday = data['birthday']
        self.coins = data['coins']
        self.fans_badge = data['fans_badge']
        self.top_photo = data['top_photo']
        self.vip = int(data['vip']['status']) == 1
        self.vip_type = self.get_vip_type(data['vip']['type'])


class Video:
    videoInfoUrl = webApiPrefix + 'view?aid={}'  # 视频信息API，需要aid
    videoStatInfoUrl = webApiPrefix + 'archive/stat?aid={}'  # 视频状态信息API，需要aid
    videoPageListInfoUrl = playerApiPrefix + 'pagelist?aid={}'  # 视频选集信息，需要aid
    videoTagsInfoUrl = 'https://api.bilibili.com/x/tag/archive/tags?aid={}'  # 视频标签信息，需要aid
    videoDanmukuUrl = 'http://comment.bilibili.cn/{}.xml'  # 视频弹幕库，需要cid
    videoDanmukuUrl1 = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'  # 视频弹幕库，需要cid

    def __init__(self, aid):
        self.aid = aid  # AV号
        self.arcurl = 'https://www.bilibili.com/video/av{}'.format(aid)
        self.coin = 0  # 投硬币数
        self.copyright = 1  # 转载是否需要授权，默认1表示需要
        self.cover = ''  # 视频封面图地址
        self.dan_mu_count = 0  # 历史累计弹幕数
        self.description = ''  # 视频简介
        self.download_url_dict = {}  # 视频下载地址
        self.duration = 0  # 所有视频总时长（秒）
        self.favorite = 0  # 收藏人数
        self.like = 0  # 点赞数
        self.owner = {}  # 视频UP简略信息，包括mid（用户ID），name（用户昵称），face（用户头像地址）
        self.page_count = 1  # 视频选集数
        self.page_list = []  # 视频选集
        self.reply = 0  # 评论数
        self.share = 0  # 分享数
        self.cid = 0  # 视频源及弹幕编号
        self.tid = 0  # 视频标签ID
        self.tag = ''  # 视频标签名
        self.title = ''  # 视频标题
        self.upload_time = 0  # 视频上传时间，unix时间戳
        self.view = 0  # 访问观看数

        # # 未赋值和使用
        # self.credit = None  # 评分数量
        # self.spid = None  # 专题SPID
        # self.offsite = None  # Flash播放调用地址
        # self.subtitle = None  # 副标题，很多视频没有
        # self.arcurl = None  # 网页地址
        # self.index = None  # 剧番中的集数
        # self.episode = None  # 集数【注：不是所有专题视频都有此信息】
        # self.episode_id = None
        # self.online_user = None  # 当前在线观看人数
        # self.partition_index = None  # 属于分P视频的索引
        # self.play_site = None  # 网站播放
        # self.play_forward = None  # 外链播放？
        # self.play_mobile = None  # app播放

        self.sess = requests.Session()

        self._get_video_info()

    def __getattr__(self, name):  # 定义当用户试图获取一个不存在的属性时的行为
        return None

    def __str__(self):  # 定义当被str()调用或者打印对象时的行为
        return str(self.__dict__)  # 返回当前范围（类或实例）的所有属性名称列表

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def _get_video_info(self):
        """
        获取视频信息

        API返回示例：
        {
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data": {
                "aid": 41043923,
                "videos": 1,  # 视频选集数量
                "tid": 17,  # 标签ID
                "tname": "单机游戏",  # 标签名
                "copyright": 1,  # 转载是否需要授权
                "pic": "http://i2.hdslb.com/bfs/archive/1b413d6624d03748f8c9c910ef75309d4d7a58b6.jpg",  # 封面图地址
                "title": "求生之路2《死亡陷阱Deadenator》专家8特单通+++",  # 视频标题
                "pubdate": 1547803629,  # 上传时间
                "ctime": 1547803629,
                "desc": "三方图死亡陷阱专家8特单通！！！",  # 视频简介
                "state": 0,
                "attribute": 2113920,
                "duration": 1596,  # 所有视频的总时长（秒）
                "rights": {  # 设置相关
                    "bp": 0,
                    "elec": 0,
                    "download": 1,
                    "movie": 0,
                    "pay": 0,
                    "hd5": 1,
                    "no_reprint": 1,
                    "autoplay": 1,
                    "ugc_pay": 0,
                    "is_cooperation": 0
                },
                "owner": {  # 用户信息
                    "mid": 19044889,  # 用户ID
                    "name": "pc迷你猪",  # 用户昵称
                    "face": "http://i2.hdslb.com/bfs/face/c8eaab28e4c057c1f172e604c93c74ff6c23040b.jpg"  # 用户头像地址
                },
                "stat": {
                    "aid": 41043923,
                    "view": 28937,
                    "danmaku": 1229,
                    "reply": 206,
                    "favorite": 358,
                    "coin": 1900,
                    "share": 67,
                    "now_rank": 0,
                    "his_rank": 0,
                    "like": 1682,
                    "dislike": 0
                },
                "dynamic": "#求生之路2##求生之路##单通#",
                "cid": 72094604,
                "dimension": {
                    "width": 1920,
                    "height": 1080,
                    "rotate": 0
                },
                "no_cache": false,
                "pages": [{
                        "cid": 72094604,
                        "page": 1,
                        "from": "vupload",
                        "part": "死亡陷阱",
                        "duration": 1596,
                        "vid": "",
                        "weblink": "",
                        "dimension": {
                            "width": 1920,
                            "height": 1080,
                            "rotate": 0
                        }
                    }
                ],
                "subtitle": {
                    "allow_submit": false,
                    "list": []
                }
            }
        }
        """
        url = self.videoInfoUrl.format(self.aid)
        json_info = get_json_info(url)
        data = json_info.get_value('data')
        self.page_count = data['videos']
        self.cid = data['cid']
        self.tid = data['tid']
        self.tag = data['tname']
        self.copyright = data['copyright']
        self.cover = data['pic']
        self.title = data['title']
        self.upload_time = data['pubdate']
        self.description = data['desc']
        self.duration = data['duration']
        self.owner = data['owner']

        self._get_video_stat_info()

        self._get_video_page_list_info()

    def _get_video_stat_info(self):
        """
        获取视频状态信息
        :return None

        API返回示例：
        code: 0
        data: {
            aid: 41025837  # AV号
            coin: 163738  # 投硬币数
            copyright: 1  # 转载是否需要授权，1表示需要
            danmaku: 12547  # 历史累计弹幕数
            favorite: 59138  # 收藏人数
            his_rank: 0  # 排行，暂未发现用处
            like: 129160  # 点赞数
            no_reprint: 1  # 未知
            now_rank: 0  # 当前排行，暂未发现用处
            reply: 4362  # 评论数
            share: 3587  # 分享数
            view: 765931  # 查看数
        }
        message: "0"
        ttl: 1
        """
        url = self.videoStatInfoUrl.format(self.aid)
        json_info = get_json_info(url)
        data = json_info.get_value('data')
        self.coin = data['coin']
        self.copyright = data['copyright']
        self.dan_mu_count = data['danmaku']
        self.favorite = data['favorite']
        self.like = data['like']
        self.reply = data['reply']
        self.share = data['share']
        self.view = data['view']

    def _get_video_page_list_info(self):
        """
        获取视频选集信息

        API返回示例：
        {
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data": [{
                    "cid": 67112764,
                    "page": 1,  # 第几P
                    "from": "vupload",  # 视频来源，vupload 应该是up自己上传的
                    "part": "第一章（1/5）",  # 选集名称
                    "duration": 3716,  # 视频时长（秒）
                    "vid": "",
                    "weblink": "",
                    "dimension": {
                        "width": 1920,  # 视频宽
                        "height": 1080,  # 视频高
                        "rotate": 0  # 视频旋转角度
                    }
                },...
            ]
        }
        """
        url = self.videoPageListInfoUrl.format(self.aid)
        json_info = get_json_info(url)
        data = json_info.get_value('data')
        for x in data:
            temp = VideoPage(x['cid'], page=x['page'], origin=x['from'], part=x['part'], duration=x['duration'],
                             width=x['dimension']['width'], height=x['dimension']['height'],
                             rotate=x['dimension']['rotate'])
            self.page_list.append(temp)

    @staticmethod
    def _check_dir(directory):
        """
        基于Windows环境，检查输入路径的合法性并过滤非法字符
        检查路径仅考虑目标存在的情况，因为目标不存在时均返回False
        windows下文件名非法字符如下: / \ : * " < > |
        :return: True
        """
        try:
            if os.path.isfile(directory):
                raise ValueError('路径不能为文件')
            if os.path.islink(directory):
                raise ValueError('路径不能为链接')
            if os.path.ismount(directory):
                raise ValueError('路径不能为根路径')

            if directory != '.' and directory != '..':
                if not os.path.isabs(directory) and directory not in os.listdir('.'):
                    """
                    os.path.isabs(path)
                    判断是否为绝对路径

                    os.listdir()
                    用于返回指定的文件夹包含的文件或文件夹的名字的列表。
                    这个列表以字母顺序排序。 它不包括 '.' 和'..' 即使它在文件夹中。
                    只支持在 Unix, Windows 下使用。
                    参数:
                        path -- 需要列出的目录路径
                    返回：
                        返回指定路径下的文件和文件夹列表。

                    os.mkdir()
                    用于以数字权限模式创建目录。默认的模式为 0777 (八进制)。
                    参数：
                        path -- 要创建的目录
                        mode -- 要为目录设置的权限数字模式
                    返回：
                        该方法没有返回值。
                    """
                    directory = re.sub(r'[\\/|<>:"*?]', '_', directory)
                    os.mkdir(directory)

                if os.path.isabs(directory) and not os.path.exists(directory):
                    """
                    os.path.exists(path)
                    如果路径 path 存在，返回 True；如果路径 path 不存在，返回 False。

                    os.makedirs(path, mode=0o777)
                    用于递归创建目录。像mkdir(), 但创建的所有intermediate-level文件夹需要包含子目录。
                    参数
                        path -- 需要递归创建的目录。
                        mode -- 权限模式。
                    返回值
                        该方法没有返回值。
                    """
                    directory = re.sub(r'[|<>"*?]', '_', directory)
                    os.makedirs(directory)

        except Exception as e:
            exit(e)
        else:
            return directory

    @staticmethod
    def _get_video_quality_info(cid):
        """
        获取视频清晰度
        :return None

        API返回示例：
        {
            'from': 'local',
            'result': 'suee',
            'quality': 16,
            'format': 'flv360',
            'timelength': 600454,
            'accept_format': 'flv,flv720,flv480,flv360',
            'accept_description': ['高清 1080P', '高清 720P', '清晰 480P', '流畅 360P'],
            'accept_quality': [80, 64, 32, 16],
            'video_codecid': 7,
            'video_project': False,
            'seek_param': 'start',
            'seek_type': 'offset',
            'durl': [{
                    'order': 1,
                    'length': 360453,
                    'size': 5778952,
                    'ahead': 'K5IIAA==',
                    'vhead': 'AWQAHv/hABpnZAAerNlAoC/5cBEAAAMAAQAAAwAoDxYtlgEABWjr7PI8',
                    'url': 'http://upos-hz-mirrorkodou.acgvideo.com/upgcxcode/84/90/41239084/41239084-1-15.flv?e=ig8euxZM2rNcNbKVhwdVtWKVhwdVNEVEuCIv29hEn0lqXg8Y2ENvNCImNEVEUJ1miI7MT96fqj3E9r1qNCNEto8g2ENvN03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1549478236&gen=playurl&nbs=1&oi=2883558202&os=kodou&platform=pc&trid=ac7cd98b4fb54b3cbc1477361ef510c3&uipk=5&upsig=7825166fcc24b00d65db6c41559f2d26',
                    'backup_url': ['http://upos-hz-mirrorcos.acgvideo.com/upgcxcode/84/90/41239084/41239084-1-15.flv?um_deadline=1549478236&platform=pc&rate=40000&oi=2883558202&um_sign=2eec752bbc68b23bb8cdaaef04540f5f&gen=playurl&os=cos&trid=ac7cd98b4fb54b3cbc1477361ef510c3']
                }, {
                    'order': 2,
                    'length': 240001,
                    'size': 4072335,
                    'url': 'http://upos-hz-mirrorwcsu.acgvideo.com/upgcxcode/84/90/41239084/41239084-2-15.flv?e=ig8euxZM2rNcNbKVhwdVtWKVhwdVNEVEuCIv29hEn0lqXg8Y2ENvNCImNEVEUJ1miI7MT96fqj3E9r1qNCNEto8g2ENvN03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1549478236&gen=playurl&nbs=1&oi=2883558202&os=wcsu&platform=pc&trid=ac7cd98b4fb54b3cbc1477361ef510c3&uipk=5&upsig=eefe802a1907f5ac1ce93601c93455f9',
                    'backup_url': ['http://upos-hz-mirrorcos.acgvideo.com/upgcxcode/84/90/41239084/41239084-2-15.flv?um_deadline=1549478236&platform=pc&rate=40000&oi=2883558202&um_sign=774de87f164e365d21b760dd16b4def7&gen=playurl&os=cos&trid=ac7cd98b4fb54b3cbc1477361ef510c3']
                }
            ]
        }
        """
        params = {'cid': cid, 'otype': 'json', 'qn': 15, 'quality': 15, 'type': ''}
        url = signApiUrl + get_sign(params)
        json_info = get_json_info(url)
        return json_info.get_value('accept_quality')

    def _get_video_download_url(self):
        """
        {
            'code': 0,
            'message': '0',
            'ttl': 1,
            'data': {
                'from': 'local',
                'result': 'suee',
                'message': '',
                'quality': 32,
                'format': 'flv480',
                'timelength': 73880,
                'accept_format': 'hdflv2,flv,flv720,flv480,flv360',
                'accept_description': ['高清 1080P+', '高清 1080P', '高清 720P', '清晰 480P', '流畅 360P'],
                'accept_quality': [112, 80, 64, 32, 16],
                'video_codecid': 7,
                'seek_param': 'start',
                'seek_type': 'offset',
                'durl': [{
                        'order': 1,
                        'length': 73880,
                        'size': 9734400,
                        'ahead': 'EhA=',
                        'vhead': 'AWQAH//hABlnZAAfrNlA2D3n4QAAAwABAAADADwPGDGWAQAEaOvvLA==',
                        'url': 'http://cn-ahhn-cmcc-v-02.acgvideo.com/upgcxcode/01/07/72780701/72780701-1-32.flv?expires=1548265200&platform=pc&ssig=jJduh_X2hMD9kxpqI2FHPQ&oi=3084752436&nfa=BpfiWF+i4mNW8KzjZFHzBQ==&dynamic=1&hfa=2122024342&hfb=Yjk5ZmZjM2M1YzY4ZjAwYTMzMTIzYmIyNWY4ODJkNWI=&trid=4b82ce92f0fb48d790f2e604a5fc96a2&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1',
                        'backup_url': ['http://upos-hz-mirrorkodo.acgvideo.com/upgcxcode/01/07/72780701/72780701-1-32.flv?e=ig8euxZM2rNcNbhg7zUVhoMzhbuBhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==&deadline=1548265381&dynamic=1&gen=playurl&oi=3084752436&os=kodo&platform=pc&rate=327500&trid=4b82ce92f0fb48d790f2e604a5fc96a2&uipk=5&uipv=5&um_deadline=1548265381&um_sign=475ec09d5a26cba21714775feeaf8f2c&upsig=c021b0e546e700de35d9b1b6dc0cb9e4', 'http://upos-hz-mirrorcos.acgvideo.com/upgcxcode/01/07/72780701/72780701-1-32.flv?um_deadline=1548265381&platform=pc&rate=327500&oi=3084752436&um_sign=475ec09d5a26cba21714775feeaf8f2c&gen=playurl&os=cos&trid=4b82ce92f0fb48d790f2e604a5fc96a2']
                    }
                ]
            },
            'session': '4873680f4128236a8d208fdec0024ac3',
            'videoFrame': {}
        }
        """
        for p in self.page_list:
            url = self.arcurl + '?p=' + str(p.page)

            req = get_url_content(url)
            encode_type = chardet.detect(req)  # 获取编码方式
            req = req.decode(encode_type['encoding'], 'ignore')  # 根据编码方式解码
            pattern = '.__playinfo__=(.*)</script><script>window.__INITIAL_STATE__='
            try:
                infos = get_re(pattern, req)[0]
            except Exception as e:
                print(e)
                return None

            json_info = json.loads(infos)
            durl = json_info['data']['durl']
            for i in range(len(durl)):
                url = durl[i]['url']

                if str(p.cid) not in self.download_url_dict:
                    self.download_url_dict[str(p.cid)] = []

                self.download_url_dict[str(p.cid)].append(url)

    def _get_video_download_url_v2(self):
        """
        获取视频下载地址
        :return None

        API返回示例：
        {
            'from': 'local',
            'result': 'suee',
            'quality': 16,
            'format': 'flv360',
            'timelength': 600454,
            'accept_format': 'flv,flv720,flv480,flv360',
            'accept_description': ['高清 1080P', '高清 720P', '清晰 480P', '流畅 360P'],
            'accept_quality': [80, 64, 32, 16],
            'video_codecid': 7,
            'video_project': False,
            'seek_param': 'start',
            'seek_type': 'offset',
            'durl': [{
                    'order': 1,
                    'length': 360453,
                    'size': 5778952,
                    'ahead': 'K5IIAA==',
                    'vhead': 'AWQAHv/hABpnZAAerNlAoC/5cBEAAAMAAQAAAwAoDxYtlgEABWjr7PI8',
                    'url': 'http://upos-hz-mirrorkodou.acgvideo.com/upgcxcode/84/90/41239084/41239084-1-15.flv?e=ig8euxZM2rNcNbKVhwdVtWKVhwdVNEVEuCIv29hEn0lqXg8Y2ENvNCImNEVEUJ1miI7MT96fqj3E9r1qNCNEto8g2ENvN03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1549478236&gen=playurl&nbs=1&oi=2883558202&os=kodou&platform=pc&trid=ac7cd98b4fb54b3cbc1477361ef510c3&uipk=5&upsig=7825166fcc24b00d65db6c41559f2d26',
                    'backup_url': ['http://upos-hz-mirrorcos.acgvideo.com/upgcxcode/84/90/41239084/41239084-1-15.flv?um_deadline=1549478236&platform=pc&rate=40000&oi=2883558202&um_sign=2eec752bbc68b23bb8cdaaef04540f5f&gen=playurl&os=cos&trid=ac7cd98b4fb54b3cbc1477361ef510c3']
                }, {
                    'order': 2,
                    'length': 240001,
                    'size': 4072335,
                    'url': 'http://upos-hz-mirrorwcsu.acgvideo.com/upgcxcode/84/90/41239084/41239084-2-15.flv?e=ig8euxZM2rNcNbKVhwdVtWKVhwdVNEVEuCIv29hEn0lqXg8Y2ENvNCImNEVEUJ1miI7MT96fqj3E9r1qNCNEto8g2ENvN03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1549478236&gen=playurl&nbs=1&oi=2883558202&os=wcsu&platform=pc&trid=ac7cd98b4fb54b3cbc1477361ef510c3&uipk=5&upsig=eefe802a1907f5ac1ce93601c93455f9',
                    'backup_url': ['http://upos-hz-mirrorcos.acgvideo.com/upgcxcode/84/90/41239084/41239084-2-15.flv?um_deadline=1549478236&platform=pc&rate=40000&oi=2883558202&um_sign=774de87f164e365d21b760dd16b4def7&gen=playurl&os=cos&trid=ac7cd98b4fb54b3cbc1477361ef510c3']
                }
            ]
        }
        """
        for p in self.page_list:
            quality = self._get_video_quality_info(p.cid)
            params = {'cid': p.cid, 'otype': 'json', 'qn': quality[0], 'quality': quality[0], 'type': ''}
            url = signApiUrl + get_sign(params)
            json_info = get_json_info(url)
            durl = json_info.get_value('durl')
            for i in range(len(durl)):
                url = durl[i]['url']

                if str(p.cid) not in self.download_url_dict:
                    self.download_url_dict[str(p.cid)] = []

                self.download_url_dict[str(p.cid)].append(url)

    def video_downloader(self, directory, download_url, file_name):
        """
        视频下载器
        :param directory: 视频保存路径
        :param download_url: 视频下载地址
        :param file_name: 保存的视频名称
        :return None
        """
        size = 0
        download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': self.arcurl
        }
        """
        contextlib.closing(thing)
        返回一个在块完成上结束thing的上下文管理器。
        无需明确关闭thing。即使发生错误， thing.close()也会在with退出块时调用。

        with语句体执行之前运行__enter__方法，在with语句体执行完后运行__exit__方法。
        如果一个类没有这两个方法，是无法使用with的。 
        contextlib.closing()会帮它加上__enter__()和__exit__()，使其满足with的条件。
        """
        with closing(self.sess.get(download_url, headers=download_headers, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                # sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
                video_name = os.path.join(directory, file_name)
                with tqdm(total=content_size, mininterval=1, unit='Bytes') as bar:
                    bar.set_description('[Download]')
                    with open(video_name, 'wb') as file:
                        """
                        requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，
                        可以用Response.iter_content来边下载边存硬盘，
                        chunk_size可以自由调整为可以更好地适合您的用例的数字
    
                        对于分块的编码请求，我们最好使用 Response.iter_content()对其数据进行迭代。
                        在理想情况下，你的 request 会设置 stream=True，
                        这样你就可以通过调用 iter_content 并将分块大小参数设为 None，从而进行分块的迭代。
                        如果你要设置分块的最大体积，你可以把分块大小参数设为任意整数。
                        """
                        for data in response.iter_content(chunk_size=chunk_size):
                            """
                            write() 方法用于向文件中写入指定字符串。
                            在文件关闭前或缓冲区刷新前，字符串内容存储在缓冲区中，这时你在文件中是看不到写入的内容的。
                            如果文件打开模式带 b，那写入文件内容时，str (参数)要用 encode 方法转为 bytes 形式，
                            否则报错：TypeError: a bytes-like object is required, not 'str'。
                            """
                            file.write(data)
                            size += len(data)
                            """
                            flush() 方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，同时清空缓冲区，不需要被动的等待输出缓冲区写入。
                            一般情况下，文件关闭后会自动刷新缓冲区，但有时你需要在关闭前刷新它，这时就可以使用 flush() 方法。
                            """
                            file.flush()

                            bar.update(len(data))  # 更新下载进度条
                            # sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                            # sys.stdout.flush()
                if size / content_size == 1:
                    print('视频[{}]下载完成!'.format(file_name))
            else:
                print('链接异常')

    @exec_time
    def download_video(self, directory=r'video', stage_width=640, stage_height=360, **kwargs):
        """
        单线程下载视频及弹幕
        :param directory: 下载目录
        :param stage_width: 弹幕宽
        :param stage_height: 弹幕高
        :param kwargs: 其余下载弹幕时用的参数
        :return: None
        """
        new_directory = self._check_dir(directory)  # 检查目录合法性
        print('>>>目录检查完成...')

        self._get_video_download_url_v2()  # 获取视频下载地址
        print('>>>获取视频下载地址完成...')

        # 下载视频
        page_list_length = len(self.page_list)  # 视频分P总数
        for i in range(page_list_length):
            # 针对多p视频的标题处理
            if page_list_length == 1:
                title = self.title
            else:
                title = self.title + '_' + self.page_list[i].part

            for c in u'´☆❤◦\/:*?"<>|':  # 过滤文件非法字符
                title = title.replace(c, '')

            title = title.replace(' ', '_')  # 转换空格，避免ffmpeg无法识别

            if title + '.flv' not in os.listdir(new_directory):
                movies = []
                cid_ = str(self.page_list[i].cid)
                for i_, url_ in enumerate(self.download_url_dict[cid_]):
                    if url_ != '':
                        temp_file_name = title + '_' + str(i_ + 1) + '.flv'
                        movies.append(temp_file_name)
                        print('视频[{}]下载中...'.format(temp_file_name))
                        self.video_downloader(new_directory, url_, temp_file_name)

                # 多段视频合成
                if len(movies) > 1:
                    try:
                        """
                        os.path.join(path1[, path2[, ...]])
                        把目录和文件名合成一个路径，可以传入多个路径
                        会从第一个以”/”开头的参数开始拼接，之前的参数全部丢弃。
                        在上一种情况确保情况下，若出现”./”开头的参数，从”./”开头的参数前的全部会保留并开始拼接。
                        """
                        file_list_file_name = os.path.join(new_directory, 'file_list.txt')

                        with open(file_list_file_name, 'w') as f:
                            for flv in movies:
                                f.write("file " + flv)
                                f.write('\n')

                        os.system('cd %s & ffmpeg -f concat -safe 0 -i %s -c copy %s' % (
                            new_directory, 'file_list.txt', title + '.flv'))

                        """
                        os.remove(path)
                        用于删除指定路径的文件。如果指定的路径是一个目录，将抛出OSError。
                        参数
                            path -- 要移除的文件路径
                        返回值
                            该方法没有返回值
                        """
                        for movie in movies:
                            os.remove(os.path.join(new_directory, movie))

                        os.remove(file_list_file_name)

                        print('视频合并完成！')
                    except Exception as e:
                        exit(e)
                else:
                    """
                    os.rename(src, dst)
                    用于命名文件或目录，从 src 到 dst,如果dst是一个存在的目录, 将抛出OSError。
                    只能对相应的文件进行重命名, 不能重命名文件的上级目录名。
                    参数
                        src -- 要修改的目录名
                        dst -- 修改后的目录名
                    返回值
                        该方法没有返回值

                    os.renames(old, new)
                    用于递归重命名目录或文件。
                    是os.rename的升级版, 既可以重命名文件, 也可以重命名文件的上级目录名。
                    参数
                        old -- 要重命名的目录
                        new --文件或目录的新名字。甚至可以是包含在目录中的文件，或者完整的目录树。
                    返回值
                        该方法没有返回值
                    """
                    os.rename(os.path.join(new_directory, movies[0]), os.path.join(new_directory, title + '.flv'))

                # 下载弹幕文件
                danmu_ass = os.path.join(new_directory, title + '.ass')
                print('视频[{}]的弹幕下载中...'.format(title))
                self.get_video_danmuku_2_ass(cid_, danmu_ass, stage_width, stage_height, **kwargs)
                print('视频[{}]的弹幕下载完成!'.format(title))

        print('>>>视频全部下载完成！')

    @exec_time
    def multi_thread_download_video(self, directory=r'video', stage_width=640, stage_height=360, **kwargs):
        """
        单线程下载视频及弹幕
        :param directory: 下载目录
        :param stage_width: 弹幕宽
        :param stage_height: 弹幕高
        :param kwargs: 其余下载弹幕时用的参数
        :return: None
        """
        new_directory = self._check_dir(directory)  # 检查目录合法性
        print('>>>目录检查完成...')

        self._get_video_download_url_v2()  # 获取视频下载地址
        print('>>>获取视频下载地址完成...')

        page_list_length = len(self.page_list)
        max_workers = page_list_length if cpu_count() > page_list_length else cpu_count()
        semaphore = threading.BoundedSemaphore(max_workers)

        all_tasks = [MultiThreadDownloadVideo(self, semaphore, i, new_directory, stage_width, stage_height, **kwargs)
                     for i in range(page_list_length)]
        for task in all_tasks:
            task.start()

        for task in all_tasks:
            task.join()

        print('>>>视频全部下载完成！')

    async def _async_video_downloader(self, semaphore: asyncio.Semaphore, directory, download_url, file_name):
        """
        异步视频下载器，不下载弹幕，因为弹幕使用的是阻塞IO，无法应用协程
        :param semaphore: 同时进行的最大协程数
        :param directory: 视频保存路径
        :param download_url: 视频下载地址
        :param file_name: 保存的视频名称
        :return None
        """
        download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': self.arcurl
        }

        size = 0
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url, headers=download_headers, chunked=True, verify_ssl=False) as response:
                    chunk_size = 1024 * 1024
                    content_size = int(response.headers['content-length'])
                    if response.status == 200:
                        video_name = os.path.join(directory, file_name)
                        async with aiofiles.open(video_name, 'wb') as file:
                            async for data in response.content.iter_chunked(chunk_size):
                                await file.write(data)
                                size += len(data)
                                await file.flush()

                        if size / content_size == 1:
                            print('视频[{}]下载完成!'.format(file_name))

    async def _async_download_video(self, i: int, queue: asyncio.Queue, semaphore: asyncio.Semaphore, directory=r'video'):
        """
        单线程下载视频及弹幕
        :param i: 任务下标
        :param queue: 清理队列
        :param semaphore: 同时进行的最大协程数
        :param directory: 下载目录
        :return: None
        """
        # 针对多p视频的标题处理
        if len(self.page_list) == 1:
            title = self.title
        else:
            title = self.title + '_' + self.page_list[i].part

        for c in u'´☆❤◦\/:*?"<>|':  # 过滤文件非法字符
            title = title.replace(c, '')

        title = title.replace(' ', '_')  # 转换空格，避免ffmpeg无法识别

        if title + '.flv' not in os.listdir(directory):
            movies = []
            cid_ = str(self.page_list[i].cid)
            for i_, url_ in enumerate(self.download_url_dict[cid_]):
                if url_ != '':
                    temp_file_name = title + '_' + str(i_ + 1) + '.flv'
                    movies.append(temp_file_name)
                    print('视频[{}]下载中...'.format(temp_file_name))
                    await self._async_video_downloader(semaphore, directory, url_, temp_file_name)

            await asyncio.sleep(1)  # 等待释放相关资源以供ffmpeg使用

            # 多段视频合成
            if len(movies) > 1:
                try:
                    file_list_file_name = os.path.join(directory, 'file_list_' + str(i + 1) + '.txt')
                    async with aiofiles.open(file_list_file_name, 'w') as f:
                        for flv in movies:
                            await f.write("file " + flv)
                            await f.write('\n')

                    """
                    ffmpeg
                    -i path（输入）
                    输入您要处理的视频文件路径

                    -f fmt（输入/输出）
                    强制输入或输出文件格式。通常会自动检测输入文件的格式，并从输出文件的文件扩展名中猜出格式，因此在大多数情况下不需要此选项。

                    -c [：stream_specifier ] 编解码器（输入/输出，每个流）
                    为一个或多个流选择编码器（在输出文件之前使用时）或解码器（在输入文件之前使用时）。
                    codec是解码器/编码器的名称或特殊值copy（仅输出），表示不对流进行重新编码。

                    例如
                    ffmpeg -i INPUT -map 0 -c:v libx264 -c:a copy OUTPUT
                    使用libx264对所有视频流进行编码并复制所有音频流。

                    对于每个流，c应用最后一个匹配选项，因此
                    ffmpeg -i INPUT -map 0 -c copy -c：v：1 libx264 -c：a：137 libvorbis OUTPUT
                    将复制除第二个视频（将使用libx264编码）和第138个音频（将使用libvorbis编码）之外的所有流。
                    """
                    cwd = directory if os.path.isabs(directory) else os.path.join(sys.path[0], directory)
                    process = subprocess.Popen(
                        ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list_' + str(i + 1) + '.txt', '-c', 'copy',
                         title + '.flv'], cwd=cwd)

                    while True:
                        if process.poll() is not None:  # 等待子进程结束
                            queue.put_nowait(file_list_file_name)
                            for movie in movies:
                                queue.put_nowait(os.path.join(directory, movie))
                            break

                        await asyncio.sleep(1)
                except Exception as e:
                    print(e)
            else:
                os.rename(os.path.join(directory, movies[0]), os.path.join(directory, title + '.flv'))
        else:
            return None

    @exec_time
    def async_download_video(self, directory=r'video'):
        new_directory = self._check_dir(directory)  # 检查目录合法性
        print('>>>目录检查完成...')

        self._get_video_download_url_v2()  # 获取视频下载地址
        print('>>>获取视频下载地址完成...')

        futures = []
        clean_queue = asyncio.Queue()
        page_list_length = len(self.page_list)
        max_workers = page_list_length if cpu_count() * 2 > page_list_length else cpu_count() * 2
        current_semaphore = asyncio.Semaphore(max_workers)  # 限制并发量为任务数或CPU核数的2倍
        for i in range(page_list_length):
            futures.append(self._async_download_video(i, clean_queue, current_semaphore, new_directory))

        with closing(asyncio.get_event_loop()) as loop:
            loop.run_until_complete(asyncio.gather(*futures))

        # 清理不需要的文件
        while True:
            if not clean_queue.empty():
                os.remove(clean_queue.get_nowait())
            else:
                break

        print('>>>视频全部下载完成！')

    def get_video_danmuku(self, cid, return_type='list', order='asc'):
        """
        获取视频弹幕库
        :param cid: 视频弹幕ID
        :param return_type 返回类型，string（bytes类型的XML），list（纯弹幕列表），
                           list_by_video_time（按视频内发送时间排序的弹幕对象列表），
                           list_by_real_time（按现实发送时间排序的弹幕对象列表），
                           list_by_danmu_type（按弹幕类型排序的弹幕对象列表）
        :param order 排序方式，asc（升序），desc（降序），只对list_by_video_time，list_by_real_time，list_by_danmu_type起作用
        :return: string or list

        python3中Unicode字符串是默认格式（就是str类型），
        ASCII编码的字符串（就是bytes类型，bytes类型是包含字节值，其实不算是字符串）要在前面加操作符b或B；
        python3还有bytearray字节数组类型

        从str到bytes:调用方法encode().
        编码是把Unicode字符串以各种方式编码成为机器能读懂的ASCII字符串
        从bytes到str:调用方法decode().

        API返回示例：
        <?xml version="1.0" encoding="UTF-8"?>
        <i>
            <chatserver>chat.bilibili.com</chatserver>
            <chatid>72094604</chatid>
            <mission>0</mission>
            <maxlimit>3000</maxlimit>
            <state>0</state>
            <real_name>0</real_name>
            <source>k-v</source>
            <d p="1.44000,1,25,16777215,1547803730,0,624a2288,10832605865312258">第一条弹幕</d>
            ...
        </i>
        """
        if return_type not in ['string', 'list', 'list_by_video_time', 'list_by_real_time', 'list_by_danmu_type']:
            return_type = 'list'

        url = self.videoDanmukuUrl.format(cid)
        content = get_url_content(url)
        if len(content) > 0:
            content = zlib.decompressobj(-zlib.MAX_WBITS).decompress(content)  # 返回bytes

            if return_type == 'string':
                return content

            danmu_list = []
            if return_type == 'list':
                """
                chardet.detect(b'Hello, world!') 
                {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
                检测出的编码是ascii，注意到还有个confidence字段，表示检测的概率是1.0（即100%）。
                """
                encode_type = chardet.detect(content)  # 获取编码方式
                string = content.decode(encode_type['encoding'])  # 根据编码方式解码
                danmu_list = get_re(r'<d p=[^>]*>([^<]*)<', string)  # 过滤标签
            else:
                if order not in ['asc', 'desc']:
                    order = 'asc'
                reverse = True if order == 'desc' else False  # 排序规则，reverse = True 降序 ， reverse = False 升序（默认）。

                danmu_list.extend(self.parse_danmu(content))
                if return_type == 'list_by_video_time':
                    danmu_list = sorted(danmu_list, key=lambda x: x.t_video, reverse=reverse)
                elif return_type == 'list_by_real_time':
                    danmu_list = sorted(danmu_list, key=lambda x: x.t_stamp, reverse=reverse)
                else:
                    danmu_list = sorted(danmu_list, key=lambda x: x.type, reverse=reverse)

            return danmu_list
        else:
            return None

    def get_video_danmuku_2_ass(self, cid, output_file, stage_width, stage_height, reserve_blank=0,
                                font_face='sans-serif',
                                font_size=20.0, text_opacity=0.9, duration_marquee=10.0, duration_still=10.0,
                                comment_filter=None, is_reduce_comments=False, progress_callback=None):
        """
        获取视频的弹幕库并转换为ASS文件
        :param cid: 视频弹幕ID
        :param output_file: 输出文件路径，需要包含后缀名ASS
        :param stage_width: 弹幕宽
        :param stage_height: 弹幕高
        :param reserve_blank: 底部留空
        :param font_face: 弹幕字体类型
        :param font_size: 弹幕字体大小
        :param text_opacity: 弹幕透明度
        :param duration_marquee: 滚动弹幕显示的持续时间
        :param duration_still: 固定弹幕显示的持续时间
        :param comment_filter: 弹幕正则表达式过滤
        :param is_reduce_comments: 如果屏幕已满，是否减少弹幕数量
        :param progress_callback: 处理回调
        :return: None

        将输出文件命名为具有相同的基本名称但扩展名（.ass）的与视频不同。
        将它们放在同一目录中，大多数媒体播放器会自动加载它们。
        传递确保宽高比的danmaku2ass与您原始视频的宽高比相匹配，否则可能会出现文本变形。
        您还可以传递多个XML/JSON文件，它们将合并到一个ASS文件中。这在同时从不同网站观看danmakus时非常有用。

        eg.
        get_video_danmuku_2_ass(r'{}/Desktop/{}.ass'.format(os.path.expanduser('~'), video.title.replace(r'/', '')),
                              640, 360, 0, 'sans-serif', 18, 1.0, 10, False)
        os.path.expanduser(path)
        把path中包含的"~"和"~user"转换成用户目录
        """
        danmu_xml = output_file.split('.')[0] + '.xml'
        with open(danmu_xml, 'wb') as file:
            file.write(self.get_video_danmuku(cid, 'string'))
            file.flush()

        time.sleep(1)
        Danmaku2ASS(danmu_xml, 'Bilibili', output_file, stage_width, stage_height, reserve_blank, font_face, font_size,
                    text_opacity, duration_marquee, duration_still, comment_filter, is_reduce_comments,
                    progress_callback)
        os.remove(danmu_xml)

    @staticmethod
    def parse_danmu(dan_mu_string):
        """
        解析XML对象并返回每条弹幕
        :param dan_mu_string: 弹幕XML字符串
        :return: string
        """
        """
        xml.dom.minidom.parseString(string[, parser])
        返回一个表示string的Document对象。此方法为string创建一个StringIO对象并将其传递给parse()。
        函数的作用是将XML解析器与“DOM构建器”连接起来，该构建器可以接受来自任何SAX解析器的解析事件并将它们转换为DOM树。
        在这些函数返回之前，将完成文档的解析; 简单地说，这些函数本身并不提供解析器实现。
        获得DOM文档对象后，可以通过其属性和方法访问XML文档的各个部分。这些属性在DOM规范中定义。
        文档对象的主要属性是 documentElement属性。它为您提供了XML文档中的主要元素：包含所有其他元素的元素。

        完成DOM树后，您可以选择调用unlink()方法以鼓励尽早清除现在不需要的对象。 
        unlink()是xml.dom.minidom DOM API的特定扩展，它使节点及其后代基本上无用。

        Node.unlink()
        取消DOM中的内部引用，以便在没有循环GC的Python版本上进行垃圾收集。
        即使循环GC可用，使用它可以更快地提供大量内存，因此在不再需要DOM对象时立即调用它是很好的做法。
        这只需要在Document对象上调用，但可以在子节点上调用以丢弃该节点的子节点。

        Node.childNodes
        此节点中包含的节点列表。这是一个只读属性。

        Document.getElementsByTagName(tagName)
        搜索具有特定元素类型名称的所有后代（直接子项，子项的子项等）。

        enumerate(sequence, [start=0])
        用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
        参数
            sequence -- 一个序列、迭代器或其他支持迭代对象。
            start -- 下标起始位置。
        返回值
            返回 enumerate(枚举) 对象。
        """
        dom = xml.dom.minidom.parseString(dan_mu_string)
        comment_element = dom.getElementsByTagName('d')
        for i, comment in enumerate(comment_element):
            p = str(comment.getAttribute('p')).split(',')
            dan_mu_obj = Danmu()
            dan_mu_obj.t_video = float(p[0])
            dan_mu_obj.type = int(p[1])
            dan_mu_obj.font_size = int(p[2])
            dan_mu_obj.color = ConvertColor(int(p[3]))
            dan_mu_obj.t_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(p[4])))
            # p[5]目前固定为0
            dan_mu_obj.mid_crc = p[6]
            # p[7]应该是弹幕ID
            if len(comment.childNodes) != 0:  # [<DOM Text node "'弹幕内容'">]列表
                dan_mu_obj.content = str(comment.childNodes[0].wholeText).replace('/n', '\n')
            else:
                dan_mu_obj.content = ""
            yield dan_mu_obj


class VideoPage:
    def __init__(self, cid, page=1, origin='vupload', part='', duration=0, width=0, height=0, rotate=0):
        self.cid = cid  # 频源及弹幕编号
        self.page = page  # 第几P，默认为1
        self.origin = origin  # 视频来源，默认为vupload（应该是up自己上传的）
        self.part = part  # 选集名称，默认为空
        self.duration = duration,  # 视频时长（秒），默认为0
        self.width = width,  # 视频宽
        self.height = height,  # 视频高
        self.rotate = rotate  # 视频旋转角度


class Danmu:
    def __init__(self):
        self.t_video = None  # 弹幕发送时间（在视频内什么时间发送的弹幕，单位秒）
        self.t_stamp = None  # 弹幕发送时间（现实时间，unix时间戳转换）
        self.mid_crc = None  # 弹幕来源，值为:hex(binascii.crc32(mid))
        self.type = None  # 弹幕类型，1:滚动弹幕，5：顶端弹幕，4：底部弹幕
        self.content = None  # 弹幕内容
        self.color = None  # 弹幕颜色
        self.font_size = None  # 弹幕字体大小


class MultiThreadDownloadVideo(threading.Thread):
    def __init__(self, video: Video, semaphore: threading.BoundedSemaphore, i: int, directory=r'video', stage_width=640,
                 stage_height=360, **kwargs):
        """
        传递视频实例对象及相关下载参数，多线程切换对CPU的负荷较大，不建议使用
        :param video: 视频实例对象
        :param semaphore: 信号量
        :param i: 当前分P所在位置
        :param directory: 下载目录
        :param stage_width: 弹幕宽
        :param stage_height: 弹幕高
        :param kwargs: 其余下载弹幕时用的参数
        :return None
        """
        super().__init__()
        self.video = video
        self.semaphore = semaphore
        self.i = i
        self.directory = directory
        self.stage_width = stage_width
        self.stage_height = stage_height
        self.kwargs = kwargs

    def run(self):
        self.semaphore.acquire()

        # 针对多p视频的标题处理
        if len(self.video.page_list) == 1:
            title = self.video.title
        else:
            title = self.video.title + '_' + self.video.page_list[self.i].part

        for c in u'´☆❤◦\/:*?"<>|':  # 过滤文件非法字符
            title = title.replace(c, '')

        title = title.replace(' ', '_')  # 转换空格，避免ffmpeg无法识别

        if title + '.flv' not in os.listdir(self.directory):
            movies = []
            cid_ = str(self.video.page_list[self.i].cid)
            for i_, url_ in enumerate(self.video.download_url_dict[cid_]):
                if url_ != '':
                    temp_file_name = title + '_' + str(i_ + 1) + '.flv'
                    movies.append(temp_file_name)
                    print('视频[{}]下载中...'.format(temp_file_name))
                    self.video.video_downloader(self.directory, url_, temp_file_name)

            # 多段视频合成
            if len(movies) > 1:
                try:
                    file_list_file_name = os.path.join(self.directory, 'file_list.txt')
                    with open(file_list_file_name, 'w') as f:
                        for flv in movies:
                            f.write("file " + flv)
                            f.write('\n')

                    os.system('cd %s & ffmpeg -f concat -safe 0 -i %s -c copy %s' % (
                        self.directory, 'file_list.txt', title + '.flv'))

                    for movie in movies:
                        os.remove(os.path.join(self.directory, movie))

                    os.remove(file_list_file_name)

                    print('视频合并完成！')
                except Exception as e:
                    print('请安装FFmpeg--http://ffmpeg.org/，并配置Path环境变量')
                    exit(e)
            else:
                os.rename(os.path.join(self.directory, movies[0]), os.path.join(self.directory, title + '.flv'))

            # 下载弹幕文件
            danmu_ass = os.path.join(self.directory, title + '.ass')
            print('视频[{}]的弹幕下载中...'.format(title))
            self.video.get_video_danmuku_2_ass(cid_, danmu_ass, self.stage_width, self.stage_height, **self.kwargs)
            print('视频[{}]的弹幕下载完成!'.format(title))

        self.semaphore.release()


# if __name__ == '__main__':
#     multi_video = Video(19940317)  # 多P，下载地址数与视频分P数不一致
#     multi_video.download_video()  # 多P，共耗时：1882.2029004096985 秒，下载弹幕
#     multi_video.multi_thread_download_video(r'videos')  # 多P，共耗时：690.1146404743195 秒，下载弹幕
#     multi_video.async_download_video()  # 多P，共耗时：506.4762177467346 秒，不下载弹幕，CPU消耗较大
