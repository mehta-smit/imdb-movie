from constant.common_constant import ACTIVE
from model import UserRole, RolePermission, session, Permission


def list_user_role():
    def _get_all_role():
        user_role = session.query(
            UserRole
        ).filter(
            UserRole.is_deleted == ACTIVE
        ).all()

        return user_role if user_role else []

    def _get_role_permission(user_role_id):
        role_permission = session.query(RolePermission).filter(
            RolePermission.user_role_id == user_role_id,
            RolePermission.is_deleted == ACTIVE
        ).all()

        return role_permission if role_permission else []

    def _get_all_permission():
        permission = session.query(Permission).filter(Permission.is_deleted == ACTIVE).all()

        if not permission:
            permission = []
        return {i.id: i.name for i in permission}

    def _prepare_response():
        user_role = _get_all_role()
        permission = _get_all_permission()

        response = list()

        for role in user_role:
            role_permission = _get_role_permission(role.id)
            response.append(dict(
                role_id=role.id,
                role_name=role.role_name,
                role_permission=list(set([permission.get(rp.permission_id, "") for rp in role_permission]))
            ))

        return response

    return _prepare_response()
