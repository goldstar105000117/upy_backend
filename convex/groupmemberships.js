import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
  args: {
    id: v.id("updated_group_memberships")
  },
  handler: async (ctx, args) => {
    return await ctx.db.query("updated_group_memberships")
      .filter(q => q.eq(q.field("_id"), args.id))
      .collect();
  },
});

export const getByUserIdAndGroupId = mutation({
  args: {
    'user_id': v.float64(),
    'group_id': v.id("updated_groups")
  },
  handler: async (ctx, args) => {
    let result = await ctx.db.query("updated_group_memberships")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .filter(q => q.eq(q.field("group_id"), args.group_id))
      .collect();
    if (result.length)
      return { success: true, result: result[0] }
    return { success: false, result: '' }
  }
})

export const createGroupMemberships = mutation({
  args: {
    'user_id': v.float64(),
    'group_id': v.id("updated_groups"),
    'role': v.string(),
    'joined_at': v.string()
  },
  handler: async (ctx, args) => {
    let result = await ctx.db
      .insert("updated_group_memberships", {
        user_id: args.user_id,
        group_id: args.group_id,
        role: args.role,
        joined_at: args.joined_at
      });
    return { success: true, result };
  }
})

export const requestJoinGroup = mutation({
  args: {
    'user_id': v.float64(),
    'group_id': v.id("updated_groups"),
  },
  handler: async (ctx, args) => {
    try {
      let get_group_membership = await ctx.db.query("updated_group_memberships")
        .filter(q => q.eq(q.field("user_id"), args.user_id))
        .filter(q => q.eq(q.field("group_id"), args.group_id))
        .collect();

      if (get_group_membership.length) {
        if (get_group_membership[0]['status'] == 'declined') {
          await ctx.db.patch(get_group_membership[0]['_id'], {
            status: "pending"
          })

          return { success: true, result: get_group_membership[0]['_id'] }
        } else if(get_group_membership[0]['status'] == 'approved')
           return { success: false, result: 'The user is already approved' }
          else return { success: false, result: 'The user is admin' }
      } else {
        let result = await ctx.db
          .insert("updated_group_memberships", {
            user_id: args.user_id,
            group_id: args.group_id,
            role: 'member',
            status: "pending"
          })

        return { success: true, result }
      }
    } catch (e) {
      return { success: false, result: 'Error: ' + e?.message}
    }
  }
})

export const approveJoinGroup = mutation({
  args: {
    'user_id': v.float64(),
    'group_id': v.id("updated_groups"),
  },
  handler: async (ctx, args) => {
    try {
      let get_group_membership = await ctx.db.query("updated_group_memberships")
        .filter(q => q.eq(q.field("user_id"), args.user_id))
        .filter(q => q.eq(q.field("group_id"), args.group_id))
        .collect();

      if (get_group_membership.length) {
        if (get_group_membership[0]['status'] == 'pending' || get_group_membership[0]['status'] == 'declined') {
          await ctx.db.patch(get_group_membership[0]['_id'], {
            status: "approved"
          })

          return { success: true, result: get_group_membership[0]['_id'] }
        } else if(get_group_membership[0]['status'] == 'approved')
           return { success: false, result: 'The user is already approved' }
          else return { success: false, result: 'The user is admin' }
      } else {
        return { success: false, result: 'The user requested joining group does not exist' }
      }
    } catch (e) {
      return { success: false, result: 'Error: ' + e?.message}
    }
  }
})

export const declineJoinGroup = mutation({
  args: {
    'user_id': v.float64(),
    'group_id': v.id("updated_groups"),
  },
  handler: async (ctx, args) => {
    try {
      let get_group_membership = await ctx.db.query("updated_group_memberships")
        .filter(q => q.eq(q.field("user_id"), args.user_id))
        .filter(q => q.eq(q.field("group_id"), args.group_id))
        .collect();

      if (get_group_membership.length) {
        if (get_group_membership[0]['status'] == 'pending' || get_group_membership[0]['status'] == 'approved') {
          await ctx.db.patch(get_group_membership[0]['_id'], {
            status: "declined"
          })

          return { success: true, result: get_group_membership[0]['_id'] }
        } else if(get_group_membership[0]['status'] == 'declined')
           return { success: false, result: 'The user is already declined' }
          else return { success: false, result: 'The user is admin' }
      } else {
        return { success: false, result: 'The user requested joining group does not exist' }
      }
    } catch (e) {
      return { success: false, result: 'Error: ' + e?.message}
    }
  }
})

export const leaveGroup = mutation({
  args: {
    'user_id': v.float64(),
    'group_id': v.id("updated_groups"),
  },
  handler: async (ctx, args) => {
    try {
      let get_group_membership = await ctx.db.query("updated_group_memberships")
        .filter(q => q.eq(q.field("user_id"), args.user_id))
        .filter(q => q.eq(q.field("group_id"), args.group_id))
        .collect();

      if (get_group_membership.length) {
        if (get_group_membership[0]['role'] == 'admin') {
          return { success: false, result: 'admin cannot leave group' }
        }
        await ctx.db.delete(args.id);
        return { success: true, result: 'Leaved group successfully' }
      } else {
        return { success: false, result: 'The user requested leaving group does not exist' }
      }
    } catch (e) {
      return { success: false, result: 'Error: ' + e?.message}
    }
  }
})

export const transferOwnership = mutation({
  args: {
    'user_id': v.float64(),
    'group_id': v.id("updated_groups"),
    'new_admin_id': v.float64()
  },
  handler: async (ctx, args) => {
    try {
      let get_group_membership = await ctx.db.query("updated_group_memberships")
        .filter(q => q.eq(q.field("user_id"), args.user_id))
        .filter(q => q.eq(q.field("group_id"), args.group_id))
        .collect();
      let new_admin_membership = await ctx.db.query("updated_group_memberships")
        .filter(q => q.eq(q.field("user_id"), args.new_admin_id))
        .filter(q => q.eq(q.field("group_id"), args.group_id))
        .collect();

      if (get_group_membership.length) {
        if (get_group_membership[0]['role'] == 'manager') {
          // await ctx.db.patch(get_group_membership[0]['_id'], {
          //   role: "member"
          // })
          // await ctx.db.patch(new_admin_membership[0]['_id'], {
          //   role: "admin"
          // })
          return { success: true, result: 'Transferred group ownership successfully' }
        } else if(get_group_membership[0]['status'] == 'declined')
           return { success: false, result: 'The user is already declined' }
          else return { success: false, result: 'The user is admin' }
      } else {
        return { success: false, result: 'The user requested joining group does not exist' }
      }
    } catch (e) {
      return { success: false, result: 'Error: ' + e?.message}
    }
  }
})