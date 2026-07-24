import { useState } from "react";
import { Button } from "../components/ui/Button";
import { PageTitle } from "../components/ui/PageTitle";
import { StateMessage } from "../components/ui/StateMessage";
import { useToast } from "../components/ui/Toast";
import { PasswordForm } from "../features/admin/PasswordForm";
import { UserForm } from "../features/admin/UserForm";
import { useUsers } from "../features/admin/useUsers";
import { useAuth } from "../features/auth/AuthContext";
import { deleteUser, updateUser, type AdminUser } from "../api/users";
import { ROLE_LABELS } from "../lib/constants";
import styles from "./UsersPage.module.css";

export function UsersPage() {
  const { isAdmin, user } = useAuth();
  const { notify } = useToast();
  const { data: users, loading, error, reload } = useUsers(isAdmin);
  const [creating, setCreating] = useState(false);
  const [passwordFor, setPasswordFor] = useState<AdminUser | null>(null);

  const guard = async (action: () => Promise<unknown>) => {
    try {
      await action();
      reload();
    } catch (cause) {
      notify((cause as Error).message);
    }
  };

  const toggleBlock = (target: AdminUser) =>
    guard(() => updateUser(target.id, { is_blocked: !target.isBlocked }));

  const remove = (target: AdminUser) => {
    if (!window.confirm(`Удалить пользователя «${target.username}»?`)) {
      return;
    }
    void guard(() => deleteUser(target.id));
  };

  if (!isAdmin) {
    return (
      <section className={styles.section}>
        <StateMessage
          icon="⛔"
          title="Недостаточно прав"
          text="Раздел доступен только администратору."
        />
      </section>
    );
  }

  return (
    <section className={styles.section}>
      <div className={styles.head}>
        <div>
          <PageTitle>Пользователи</PageTitle>
          <p className={styles.hint}>Управление доступом и ролями</p>
        </div>
        <Button variant="pink" onClick={() => setCreating(true)}>
          + Добавить пользователя
        </Button>
      </div>

      {loading && <StateMessage icon="⏳" title="Загружаем пользователей…" />}
      {!loading && error && (
        <StateMessage icon="⚠️" title="Не удалось загрузить" text={error} />
      )}

      {!loading && !error && (
        <div className={styles.tableWrap}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Пользователь</th>
                <th>Роль</th>
                <th>Статус</th>
                <th className={styles.right}>Действия</th>
              </tr>
            </thead>
            <tbody>
              {users.map((item) => {
                const isSelf = item.id === user?.id;
                return (
                  <tr key={item.id}>
                    <td>
                      <div className={styles.name}>{item.username}</div>
                      <div className={styles.email}>{item.email}</div>
                    </td>
                    <td>{ROLE_LABELS[item.role] ?? item.role}</td>
                    <td>
                      <span
                        className={
                          item.isBlocked ? styles.blocked : styles.active
                        }
                      >
                        {item.isBlocked ? "Заблокирован" : "Активен"}
                      </span>
                    </td>
                    <td className={styles.right}>
                      <div className={styles.actions}>
                        <button
                          className={styles.link}
                          type="button"
                          onClick={() => setPasswordFor(item)}
                        >
                          Пароль
                        </button>
                        {!isSelf && (
                          <button
                            className={styles.link}
                            type="button"
                            onClick={() => toggleBlock(item)}
                          >
                            {item.isBlocked ? "Разблокировать" : "Заблокировать"}
                          </button>
                        )}
                        {!isSelf && (
                          <button
                            className={`${styles.link} ${styles.danger}`}
                            type="button"
                            onClick={() => remove(item)}
                          >
                            Удалить
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {creating && (
        <UserForm onClose={() => setCreating(false)} onSaved={reload} />
      )}
      {passwordFor && (
        <PasswordForm
          user={passwordFor}
          onClose={() => setPasswordFor(null)}
          onSaved={reload}
        />
      )}
    </section>
  );
}
