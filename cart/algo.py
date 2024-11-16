# 159. Longest Substring with At Most Two Distinct Characters
# def longest_two_characters(s: str) -> str:
#     ans = 0
#     d = {}
#
#     left = 0
#     for right in range(len(s)):
#         d[s[right]] = d.get(s[right], 0) + 1
#
#         while len(d) > 2:
#             d[s[left]] -= 1
#
#             if d[s[left]] == 0:
#                 del d[s[left]]
#
#             left += 1
#
#         ans = max(ans, right - left + 1)
#
#     return ans
#
# print(longest_two_characters('ccaabbb'))

def lowestCommonAncestor(self, p, q):
    seen = set()

    while p:
        seen.add(p)
        p = p.parent

    while q:
        if q in seen:
            return q

        q = q.parent



