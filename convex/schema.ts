import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  updated_userprofile: defineTable({
    auto_approve_friend_request: v.optional(v.boolean()),
    avatar: v.optional(v.string()),
    display_name: v.optional(v.string()),
    privacy_level: v.optional(v.string()),
    bio: v.optional(v.string()),
    birthday: v.optional(v.string()),
    confirmation_email_token: v.optional(v.string()),
    confirmation_phone_code: v.optional(v.string()),
    email_confirmed: v.optional(v.boolean()),
    phone_confirmed: v.optional(v.boolean()),
    enable_notification: v.optional(v.boolean()),
    gender: v.optional(v.string()),
    hide_online_status: v.optional(v.boolean()),
    last_reset: v.optional(v.string()),
    location: v.optional(v.string()),
    notification_receive_config: v.optional(v.string()),
    phone_number: v.optional(v.string()),
    token_used: v.optional(v.boolean()),
    notificationRecieveConfig: v.optional(v.string()),
    user_id: v.id("updated_users"),
    visibility: v.optional(v.string()),
    email_expire_at: v.optional(v.string()),
    phone_expire_at: v.optional(v.string())
  }),

  updated_intereststags: defineTable({ name: v.string() }),

  updated_userintereststags: defineTable({
    interestsTags_id: v.id("updated_intereststags"),
    user_id: v.id("updated_users"),
  }),

  updated_status: defineTable({
    icon: v.string(),
    name: v.string(),
  }),

  updated_tokens: defineTable({
    expired_at: v.string(),
    token: v.string(),
    type: v.string(),
    user_id: v.id("updated_users"),
  }),

  updated_userstorage: defineTable({
    file_name: v.string(),
    file_type: v.string(),
    is_shared: v.boolean(),
    is_public: v.boolean(),
    user_id: v.id("updated_users"),
  }),

  updated_friends: defineTable({
    user_id: v.id("updated_users"),
    friend_id: v.id("updated_users"),
    status: v.string(), // e.g., 'approved', 'pending', 'declined'
  }),

  updated_followers: defineTable({
    user_id: v.id("updated_users"),
    follower_id: v.id("updated_users"),
  }),

  updated_sharedimages: defineTable({
    user_id: v.id("updated_users"),
    image: v.string(),
  }),

  updated_groups: defineTable({
    name: v.string(),
    description: v.optional(v.string()),
    is_public: v.boolean(),
    organization_id: v.optional(v.id("updated_organizations")),
  }),

  updated_teams: defineTable({
    name: v.string(),
    description: v.optional(v.string()),
    is_public: v.boolean(),
    organization_id: v.id("updated_organizations"),
  }),

  updated_organizations: defineTable({
    name: v.string(),
    description: v.optional(v.string()),
    industry: v.optional(v.string()),
  }),

  updated_group_memberships: defineTable({
    user_id: v.id("updated_users"),
    group_id: v.id("updated_groups"),
    role: v.string(),  // e.g., 'member', 'admin'
    status: v.optional(v.string()), // e.g., 'approved', 'pending', 'declined'
    transferred_ownership_id: v.optional(v.id("updated_users")),
    transferred_ownership_status: v.optional(v.string()),
    joined_at: v.string(),
  }),

  updated_team_memberships: defineTable({
    user_id: v.id("updated_users"),
    team_id: v.id("updated_teams"),
    role: v.string(),  // e.g., 'member', 'admin'
    status: v.optional(v.string()), // e.g., 'approved', 'pending', 'declined'
    transferred_ownership_id: v.optional(v.id("updated_users")),
    transferred_ownership_status: v.optional(v.string()),
    joined_at: v.string(),
  }),

  updated_organization_memberships: defineTable({
    user_id: v.id("updated_users"),
    organization_id: v.id("updated_organizations"),
    role: v.string(),  // e.g., 'member', 'admin'
    status: v.optional(v.string()), // e.g., 'approved', 'pending', 'declined'
    transferred_ownership_id: v.optional(v.id("updated_users")),
    transferred_ownership_status: v.optional(v.string()),
    joined_at: v.string(),
  }),

  updated_users: defineTable({
    email: v.string(),
    password: v.string(),
    username: v.string(),
    first_name: v.optional(v.string()),
    last_name: v.optional(v.string()),
    is_active: v.optional(v.boolean()),
    last_joined_at: v.optional(v.string()),
  }),

  updated_auth_tokens: defineTable({
    user_id: v.id("updated_users"),
    access_token: v.string(),
    refresh_token: v.string(),
  }),

  updated_user_new_emails: defineTable({
    user_id: v.id("updated_users"),
    new_email: v.string()
  }),
});